from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import get_groq_response, input_pdf_setup
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def index(request):
    return render(request, "index.html")

@csrf_exempt
def submit(request):
    if request.method == "POST":
        job_description = request.POST.get("job_description")
        prompt_type = request.POST.get("prompt_type")
        uploaded_file = request.FILES.get("resume")

        if not uploaded_file or not job_description:
            return JsonResponse({"error": "Please provide both the job description and the resume file."})

        try:
            file_stream = uploaded_file.read()
            pdf_content = input_pdf_setup(file_stream)

            if not pdf_content:
                return JsonResponse({"error": "No content extracted from the PDF. Please check the file."})

            prompt = """
            You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
            Please share your professional evaluation on whether the candidate's profile aligns with the role. 
            Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements in **point-wise format**.
            """ if prompt_type == "evaluation" else """
            You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
            Your task is to evaluate the resume against the provided job description. Provide the percentage match if the resume matches
            the job description, followed by missing keywords and final thoughts in **point-wise format**.
            """

            response = get_groq_response(job_description, pdf_content, prompt)
            return JsonResponse({"response": response})

        except Exception as e:
            return JsonResponse({"error": f"Error processing the resume: {e}"})
    else:
        return JsonResponse({"error": "Invalid request method."})

# Define the `resume_upload` view
@csrf_exempt
def resume_upload(request):
    if request.method == "POST" and request.FILES.get("resume"):
        uploaded_file = request.FILES["resume"]
        file_stream = uploaded_file.read()
        
        # Assuming you are performing PDF processing in `input_pdf_setup`
        pdf_content = input_pdf_setup(file_stream)
        
        if not pdf_content:
            return JsonResponse({"error": "No content extracted from the PDF. Please check the file."})

        # You can add additional logic here, such as storing the uploaded file or performing further processing
        return JsonResponse({"message": "Resume uploaded successfully."})
    else:
        return render(request, "upload_form.html")  # Render a form to upload resume if not POST
