from django.urls import path
from .views import RegisterView, LoginView, DoctorProfileDetail, PatientProfileDetail

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('doctor-profile/', DoctorProfileDetail.as_view(), name='doctor-profile'),
    # path('patient-profile/', PatientProfileDetail.as_view(), name='patient-profile'),
]
