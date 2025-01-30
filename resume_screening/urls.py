from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("upload/", views.resume_upload, name="resume_upload"),
    path("evaluate/", views.evaluate_resume, name="evaluate_resume"),  
    path("ats-scan/", views.ats_scan, name="ats_scan"),  
    path("fetch-related/", views.fetch_related_resumes, name="fetch_related_resumes"),  # Fetch similar resumes using RAG
]
