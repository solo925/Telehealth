from django.contrib.auth.models import User
from django.db import models

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add fields specific to patients
    medical_history = models.TextField(blank=True, null=True)

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add fields specific to doctors
    specialization = models.CharField(max_length=100)
