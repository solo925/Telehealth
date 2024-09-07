from django.urls import path
from .views import register, login, logout
from.import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
]

