from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('feedback/', views.feedback, name='feedback'),
    path('success/', views.success, name='success'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('download_json/', views.download_json, name='download_json'),
]
