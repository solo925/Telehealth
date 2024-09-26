from accounts.models import DoctorProfile, PatientProfile
from django.db import models

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    room_name = models.CharField(max_length=255, blank=True, null=True)  # Twilio Video Room
    chat_service_sid = models.CharField(max_length=255, blank=True, null=True)  # Twilio Chat SID

    def __str__(self):
        return f"{self.patient.user.username} - {self.doctor.user.username} on {self.appointment_date}"
