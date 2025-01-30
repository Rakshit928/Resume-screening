from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import process_resume, store_in_chromadb, retrieve_from_chromadb, get_groq_response
import os
from dotenv import load_dotenv

load_dotenv()

def index(request):
    return render(request, "index.html")

@csrf_exempt
def evaluate_resume(request):
    if request.method == "POST":
        try:
            job_description = request.POST.get("job_description")
            uploaded_file = request.FILES.get("resume")

            if not uploaded_file or not job_description:
                return JsonResponse({"error": "Please provide both job description and resume."}, status=400)

            file_stream = uploaded_file.read()
            pdf_content = process_resume(file_stream)
            
            if not pdf_content:
                return JsonResponse({"error": "No content extracted from PDF."}, status=400)

            resume_text = pdf_content[0]["data"]
            prompt = """
            You are an experienced Technical HR Manager. Review the resume against the job description 
            and provide a professional evaluation highlighting strengths and weaknesses in point format.
            """
            
            response = get_groq_response(job_description, resume_text, prompt)
            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid method."}, status=405)

@csrf_exempt
def ats_scan(request):
    if request.method == "POST":
        try:
            job_description = request.POST.get("job_description")
            uploaded_file = request.FILES.get("resume")

            if not uploaded_file or not job_description:
                return JsonResponse({"error": "Please provide both job description and resume."}, status=400)

            file_stream = uploaded_file.read()
            pdf_content = process_resume(file_stream)
            
            if not pdf_content:
                return JsonResponse({"error": "No content extracted from PDF."}, status=400)

            resume_text = pdf_content[0]["data"]
            prompt = """
            You are an ATS system. Evaluate the resume against the job description. Provide a match percentage,
            missing keywords, and final thoughts in point format.
            """
            
            response = get_groq_response(job_description, resume_text, prompt)
            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid method."}, status=405)

@csrf_exempt
def resume_upload(request):
    if request.method == "POST" and request.FILES.get("resume"):
        try:
            uploaded_file = request.FILES["resume"]
            file_stream = uploaded_file.read()
            pdf_content = process_resume(file_stream)

            if not pdf_content:
                return JsonResponse({"error": "No content extracted from PDF."}, status=400)
            
            return JsonResponse({"message": "Resume processed successfully."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return render(request, "upload_form.html")

@csrf_exempt
def fetch_related_resumes(request):
    if request.method == "POST":
        try:
            query = request.POST.get("query")
            if not query:
                return JsonResponse({"error": "Please provide a search query."}, status=400)
            
            related_resumes = retrieve_from_chromadb(query)
            return JsonResponse({"resumes": related_resumes})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid method."}, status=405)
