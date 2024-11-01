from django.urls import path
from .views import RegisterView, LoginView, DoctorProfileDetail, PatientProfileDetail

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('profile/doctor/', DoctorProfileDetail.as_view(), name='doctor-profile'),
    # path('profile/patient/', PatientProfileDetail.as_view(), name='patient-profile'),
]
