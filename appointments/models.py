"""
The `Appointment` model represents a scheduled appointment between a patient and a doctor. It stores information such as the patient, doctor, appointment date, status, and details related to the video chat and messaging services used for the appointment.

The `STATUS_CHOICES` tuple defines the possible statuses an appointment can have, which are 'scheduled', 'completed', and 'canceled'.

The `patient` and `doctor` fields are foreign keys that link the appointment to the corresponding `PatientProfile` and `DoctorProfile` models, respectively.

The `appointment_date` field stores the date and time of the appointment.

The `status` field stores the current status of the appointment, which is chosen from the `STATUS_CHOICES` options.

The `room_name` field stores the name of the Twilio Video room used for the appointment, and the `chat_service_sid` field stores the Twilio Chat SID used for the appointment.

The `__str__` method provides a string representation of the appointment, showing the patient and doctor usernames and the appointment date.
"""
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
