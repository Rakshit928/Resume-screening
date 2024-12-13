# from django.http import JsonResponse
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from dotenv import load_dotenv
# import os
# import io
# import fitz  # PyMuPDF for text extraction
# from PIL import Image
# import pytesseract  # OCR for scanned PDFs
# from groq import Groq

# # Load environment variables
# load_dotenv()

# # Initialize Groq client
# client = Groq()

# def process_resume(file_stream):
#     """
#     This function processes the uploaded resume and returns the extracted content.
#     """
#     text_content = extract_text_from_pdf(file_stream)
#     if not text_content:
#         text_content = extract_text_from_image(file_stream)
    
#     if not text_content:
#         return []

#     return [{"data": text_content}]

# # Split content into chunks
# def split_content(content, chunk_size=1000):
#     chunks = []
#     current_chunk = ""

#     for part in content:
#         if "data" in part and part["data"]:  # Check if data exists and is not empty
#             for paragraph in part["data"].split("\n"):  # Split by newline for better granularity
#                 if len(current_chunk) + len(paragraph) > chunk_size:
#                     chunks.append(current_chunk)
#                     current_chunk = paragraph
#                 else:
#                     current_chunk += " " + paragraph

#     if current_chunk:
#         chunks.append(current_chunk.strip())

#     return chunks

# def split_job_description(input_text, chunk_size=1000):
#     return [input_text[i:i + chunk_size] for i in range(0, len(input_text), chunk_size)]

# def get_groq_response(input_text, pdf_content, prompt):
#     text_chunks = split_content(pdf_content)
#     job_chunks = split_job_description(input_text)

#     if not text_chunks:
#         return "Error: No resume content extracted."
#     if not job_chunks:
#         return "Error: No job description provided."

#     responses = []
#     for job_chunk in job_chunks:
#         for pdf_chunk in text_chunks:
#             messages = [
#                 {"role": "system", "content": "You are a professional resume evaluator and ATS specialist."},
#                 {"role": "user", "content": f"Job Description: {job_chunk}"},
#                 {"role": "assistant", "content": "Here is the evaluation of the resume based on the provided job description and prompt."},
#                 {"role": "user", "content": f"Resume Content: {pdf_chunk}\nPrompt: {prompt}"}
#             ]

#             try:
#                 completion = client.chat.completions.create(
#                     model="llama-3.2-90b-vision-preview",
#                     messages=messages,
#                     temperature=1,
#                     max_tokens=1024,
#                     top_p=1,
#                     stream=False,
#                     stop=None,
#                 )
#                 responses.append(completion.choices[0].message.content)
#             except Exception as e:
#                 return f"Error while getting response from Groq: {e}"
    
#     return " ".join(responses)

# def extract_text_from_pdf(file_stream):
#     try:
#         pdf_document = fitz.open(stream=file_stream, filetype="pdf")
#         text = ""
#         for page_num in range(pdf_document.page_count):
#             page = pdf_document.load_page(page_num)
#             text += page.get_text("text")
#         return text.strip()
#     except Exception as e:
#         return f"Error extracting text from PDF: {e}"

# def extract_text_from_image(file_stream):
#     try:
#         pdf_document = fitz.open(stream=file_stream, filetype="pdf")
#         text = ""
#         for page_num in range(pdf_document.page_count):
#             page = pdf_document.load_page(page_num)
#             image_list = page.get_images(full=True)

#             for img_index, img in enumerate(image_list):
#                 xref = img[0]
#                 base_image = pdf_document.extract_image(xref)
#                 image_bytes = base_image["image"]
#                 image = Image.open(io.BytesIO(image_bytes))
#                 text += pytesseract.image_to_string(image)

#         return text.strip()
#     except Exception as e:
#         return f"Error extracting text from scanned PDF: {e}"

# def input_pdf_setup(file_stream):
#     text_content = extract_text_from_pdf(file_stream)
#     if not text_content:
#         text_content = extract_text_from_image(file_stream)

#     if not text_content:
#         return []
#     return [{"data": text_content}]

# def index(request):
#     return render(request, "index.html")

# @csrf_exempt
# def evaluate(request):
#     if request.method == "POST":
#         job_description = request.POST.get("job_description")
#         prompt_type = request.POST.get("prompt_type")
#         uploaded_file = request.FILES.get("resume")

#         if not uploaded_file or not job_description:
#             return JsonResponse({"error": "Please provide both the job description and the resume file."})

#         try:
#             file_stream = uploaded_file.read()
#             pdf_content = input_pdf_setup(file_stream)

#             if not pdf_content:
#                 return JsonResponse({"error": "No content extracted from the PDF. Please check the file."})

#             prompt = """
#             You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
#             Please share your professional evaluation on whether the candidate's profile aligns with the role. 
#             Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements in **point-wise format**.
#             """ if prompt_type == "evaluation" else """
#             You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
#             Your task is to evaluate the resume against the provided job description. Provide the percentage match if the resume matches
#             the job description, followed by missing keywords and final thoughts in **point-wise format**.
#             """

#             response = get_groq_response(job_description, pdf_content, prompt)
#             return JsonResponse({"response": response})

#         except Exception as e:
#             return JsonResponse({"error": f"Error processing the resume: {e}"})
#     else:
#         return JsonResponse({"error": "Invalid request method."})


import io
import fitz  # PyMuPDF for text extraction
from PIL import Image
import pytesseract  # OCR for scanned PDFs
from groq import Groq

# Initialize Groq client
client = Groq()

def process_resume(file_stream):
    """
    This function processes the uploaded resume and returns the extracted content.
    """
    text_content = extract_text_from_pdf(file_stream)
    if not text_content:
        text_content = extract_text_from_image(file_stream)
    
    if not text_content:
        return []

    return [{"data": text_content}]

# Split content into chunks
def split_content(content, chunk_size=1000):
    chunks = []
    current_chunk = ""

    for part in content:
        if "data" in part and part["data"]:  # Check if data exists and is not empty
            for paragraph in part["data"].split("\n"):  # Split by newline for better granularity
                if len(current_chunk) + len(paragraph) > chunk_size:
                    chunks.append(current_chunk)
                    current_chunk = paragraph
                else:
                    current_chunk += " " + paragraph

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def split_job_description(input_text, chunk_size=1000):
    return [input_text[i:i + chunk_size] for i in range(0, len(input_text), chunk_size)]

def get_groq_response(input_text, pdf_content, prompt):
    text_chunks = split_content(pdf_content)
    job_chunks = split_job_description(input_text)

    if not text_chunks:
        return "Error: No resume content extracted."
    if not job_chunks:
        return "Error: No job description provided."

    responses = []
    for job_chunk in job_chunks:
        for pdf_chunk in text_chunks:
            messages = [
                {"role": "system", "content": "You are a professional resume evaluator and ATS specialist."},
                {"role": "user", "content": f"Job Description: {job_chunk}"},
                {"role": "assistant", "content": "Here is the evaluation of the resume based on the provided job description and prompt."},
                {"role": "user", "content": f"Resume Content: {pdf_chunk}\nPrompt: {prompt}"}
            ]

            try:
                completion = client.chat.completions.create(
                    model="llama-3.2-90b-vision-preview",
                    messages=messages,
                    temperature=1,
                    max_tokens=1024,
                    top_p=1,
                    stream=False,
                    stop=None,
                )
                responses.append(completion.choices[0].message.content)
            except Exception as e:
                return f"Error while getting response from Groq: {e}"
    
    return " ".join(responses)

def extract_text_from_pdf(file_stream):
    try:
        pdf_document = fitz.open(stream=file_stream, filetype="pdf")
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text("text")
        return text.strip()
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

def extract_text_from_image(file_stream):
    try:
        pdf_document = fitz.open(stream=file_stream, filetype="pdf")
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                text += pytesseract.image_to_string(image)

        return text.strip()
    except Exception as e:
        return f"Error extracting text from scanned PDF: {e}"

def input_pdf_setup(file_stream):
    text_content = extract_text_from_pdf(file_stream)
    if not text_content:
        text_content = extract_text_from_image(file_stream)

    if not text_content:
        return []
    return [{"data": text_content}]
