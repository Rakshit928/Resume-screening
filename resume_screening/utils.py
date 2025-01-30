from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import os
import io
import fitz
import uuid
from PIL import Image
import pytesseract
from chromadb import PersistentClient
from groq import Groq

os.environ["TOKENIZERS_PARALLELISM"] = "false"
load_dotenv()
client = Groq()
chroma_client = PersistentClient(path="./chromadb_storage")
document_store = chroma_client.get_or_create_collection(name="resume_screening")

def extract_text_from_pdf(file_stream):
    try:
        pdf_document = fitz.open(stream=file_stream, filetype="pdf")
        text = " ".join(page.get_text() for page in pdf_document)
        return text.strip()
    except Exception as e:
        return None

def extract_text_from_image(file_stream):
    try:
        pdf_document = fitz.open(stream=file_stream, filetype="pdf")
        text_parts = []
        for page in pdf_document:
            for img in page.get_images(full=True):
                image_bytes = pdf_document.extract_image(img[0])["image"]
                text_parts.append(pytesseract.image_to_string(Image.open(io.BytesIO(image_bytes))))
        return " ".join(text_parts).strip()
    except Exception as e:
        return None

def process_resume(file_stream):
    text_content = extract_text_from_pdf(file_stream) or extract_text_from_image(file_stream)
    return [{"data": text_content}] if text_content else []

def generate_chunk_id(prefix):
    return f"{prefix}_{str(uuid.uuid4())}"

def store_in_chromadb(resume_text, job_description):
    try:
        resume_id = generate_chunk_id("resume")
        job_id = generate_chunk_id("job")
        
        document_store.add(
            documents=[resume_text, job_description],
            metadatas=[
                {"type": "resume", "timestamp": str(uuid.uuid1())},
                {"type": "job_description", "timestamp": str(uuid.uuid1())}
            ],
            ids=[resume_id, job_id]
        )
        return True
    except Exception as e:
        print(f"ChromaDB storage error: {e}")
        return False

def retrieve_from_chromadb(query_text, top_k=3):
    try:
        results = document_store.query(
            query_texts=[query_text],
            n_results=top_k
        )
        return [doc for doc in results["documents"][0]] if results["documents"] else []
    except Exception as e:
        print(f"ChromaDB retrieval error: {e}")
        return []

# def get_groq_response(job_description, resume_text, prompt):
#     try:
#         if not store_in_chromadb(resume_text, job_description):
#             return "Error storing documents in database."
        
#         retrieved_resume = " ".join(retrieve_from_chromadb(job_description))
        
#         messages = [
#             {"role": "system", "content": "You are an expert resume evaluator and ATS specialist."},
#             {"role": "user", "content": f"Job Description: {job_description}"},
#             {"role": "assistant", "content": "Evaluating the resume against the job description..."},
#             {"role": "user", "content": f"Resume Content: {retrieved_resume}\nPrompt: {prompt}"}
#         ]
        
#         completion = client.chat.completions.create(
#             model="llama-3.2-90b-vision-preview",
#             messages=messages,
#             temperature=0.7,
#             max_tokens=1024
#         )
#         return completion.choices[0].message.content
#     except Exception as e:
#         return f"Error generating response: {e}"
def get_groq_response(job_description, resume_text, prompt):
    try:
        if not store_in_chromadb(resume_text, job_description):
            return "Error storing documents in database."
        
        retrieved_resume = " ".join(retrieve_from_chromadb(job_description))
        
        formatted_prompt = f"""
Based on the following job description and resume, provide a structured evaluation:

Job Description:
{job_description}

Resume Content:
{retrieved_resume}

Please provide your analysis in the following format:
- Start with a clear match percentage (if ATS evaluation)
- List key strengths as "Strength: [point]"
- List areas for improvement as "Weakness: [point]"
- Include relevant keywords missing from resume
- Conclude with final recommendation

{prompt}
"""
        
        messages = [
            {"role": "system", "content": "You are an expert resume evaluator. Provide clear, structured feedback with proper formatting."},
            {"role": "user", "content": formatted_prompt}
        ]
        
        completion = client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {e}"

def index(request):
    return render(request, "index.html")

@csrf_exempt
def evaluate(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method."})
        
    job_description = request.POST.get("job_description")
    prompt_type = request.POST.get("prompt_type")
    uploaded_file = request.FILES.get("resume")

    if not all([uploaded_file, job_description]):
        return JsonResponse({"error": "Missing required fields."})

    try:
        file_stream = uploaded_file.read()
        resume_content = process_resume(file_stream)
        
        if not resume_content:
            return JsonResponse({"error": "Failed to extract resume content."})

        prompt = (
            "Evaluate this resume against the job description, highlighting strengths and weaknesses."
            if prompt_type == "evaluation"
            else "Analyze this resume as an ATS system, providing match percentage and missing keywords."
        )

        response = get_groq_response(job_description, resume_content[0]["data"], prompt)
        return JsonResponse({"response": response})
    except Exception as e:
        return JsonResponse({"error": f"Processing error: {e}"})
