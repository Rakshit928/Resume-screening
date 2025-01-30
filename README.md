# Resume-screening
This project implements a Django-based Resume-Screening platform that automates the process of evaluating resumes against job descriptions. By utilizing a Retrieval-Augmented Generation (RAG) system, the platform improves the accuracy of evaluating resumes by retrieving relevant information from both the resume and the job description, then generating a detailed evaluation. The system analyzes resumes in PDF format, extracts relevant content using OCR (Optical Character Recognition), and compares it to the job description provided by the user.

The use of RAG ensures that the evaluation process is data-driven, leveraging external data sources, such as pre-existing job descriptions, and offering more contextually relevant insights into how a resume matches the provided job description.


![Resume-Screening Logo](demosnap.png)

1. # Title: "Resume Evaluation"
   - Purpose: Uses a Retrieval-Augmented Generation (RAG) model to compare resumes with job descriptions.

2. # Job Description Field
   - Label: "Job Description: Paste the job description here…"
   - Description: This field allows users to paste the text of a job description.
   - Functionality:
      -> By inputting a job description, the platform likely evaluates how well the resume aligns with the job requirements.

3. # Prompt Type Dropdown
   - Label: "Prompt Type:"
   - Options:
      -> Evaluation:
        => This option seems to focus on assessing the overall quality, structure, and effectiveness of the resume.
        => May include feedback on formatting, content relevancy, and skills alignment with the job description.
     -> ATS:
        => Stands for Applicant Tracking System. This option likely checks the resume's compatibility with ATS software that many recruiters use to filter resumes.
        => Ensures proper formatting, keyword density, and absence of ATS-blocking elements (like images or complex designs).
     
   - Default Selection: Evaluation is selected in the dropdown in this image.
  
4. # Resume Upload Section
   - Label: "Upload Resume (PDF):"
   - Functionality:
      -> Provides an option for users to upload their resume as a PDF file for evaluation.
   - File Restrictions:
      -> Accepts PDF format only, likely for compatibility and consistency in processing.

5. # Submit Button
   - Purpose: Once the user pastes the job description, selects the evaluation type, and uploads the resume, clicking this button initiates the evaluation process.
