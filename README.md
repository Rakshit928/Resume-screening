# Resume-screening
A Django based Resume-Screening project leverages a Large Language Model (LLM) to automate the process of evaluating resumes against job descriptions. The system analyzes resumes in PDF format, extracts relevant content using OCR (Optical Character Recognition), and compares it with the job description provided by the user. 

![Resume-Screening Logo](demosnap.png)

1. # Title: "Resume Evaluation"
   - Purpose: Clearly indicates the functionality of the platform, which is to evaluate resumes.

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
