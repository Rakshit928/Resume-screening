import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import process_resume, store_in_chromadb, get_groq_response

def index(request):
    return render(request, "index.html")

@csrf_exempt
def evaluate(request):
    if request.method == "POST":
        try:
            job_description = request.POST.get("job_description")
            uploaded_file = request.FILES.get("resume")

            if not all([uploaded_file, job_description]):
                return JsonResponse({"error": "Please provide both resume and job description"})

            content = process_resume(uploaded_file.read())
            if not content:
                return JsonResponse({"error": "Could not extract resume content"})

            prompt = """
            You are an experienced Technical HR Manager. Evaluate this resume against the job description.
            Provide: 1) Overall match assessment 2) Key strengths 3) Areas for improvement
            Format with clear sections and bullet points.
            """

            response = get_groq_response(job_description, content[0]["data"], prompt)
            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method"})

@csrf_exempt
def ats_scan(request):
    if request.method == "POST":
        try:
            job_description = request.POST.get("job_description")
            uploaded_file = request.FILES.get("resume")

            if not all([uploaded_file, job_description]):
                return JsonResponse({"error": "Please provide both resume and job description"})

            content = process_resume(uploaded_file.read())
            if not content:
                return JsonResponse({"error": "Could not extract resume content"})

            prompt = """
            You are an ATS system. Analyze this resume against the job description.
            Provide: 1) Match percentage 2) Missing keywords 3) Key qualifications 4) Recommendations
            Format with clear sections and bullet points.
            """

            response = get_groq_response(job_description, content[0]["data"], prompt)
            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method"})
