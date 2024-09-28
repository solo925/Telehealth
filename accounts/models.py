"""
The `DoctorProfile` model represents the profile information for a doctor user in the system. It is linked to the `User` model using a one-to-one relationship, allowing each doctor to have a corresponding profile.

The `PatientProfile` model represents the profile information for a patient user in the system. It is also linked to the `User` model using a one-to-one relationship, allowing each patient to have a corresponding profile.

Both the `DoctorProfile` and `PatientProfile` models override the `__str__` method to return the username of the associated user, which can be useful for string representations of these objects.
"""
from django.db import models
from django.contrib.auth.models import User

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    
    def __str__(self):
        return self.user.username
    
    

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
   
    def __str__(self):
        return self.user.username
    
