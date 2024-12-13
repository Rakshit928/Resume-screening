# urls.py
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path('submit/', views.submit, name='submit'),  # Existing URL for submit
    path('evaluate/', views.submit, name='evaluate'),  # Add this line to handle /evaluate/
    path('upload/', views.resume_upload, name='resume_upload'),
]
