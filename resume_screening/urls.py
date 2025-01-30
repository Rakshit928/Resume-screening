from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('evaluate/', views.evaluate, name='evaluate'),
    path('ats-scan/', views.ats_scan, name='ats_scan'),
]
