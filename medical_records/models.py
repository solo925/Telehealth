from django.db import models
from django.contrib.auth.models import User

class MedicalRecord(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_records')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_records')
    title = models.CharField(max_length=200)
    description = models.TextField()
    document = models.FileField(upload_to='medical_records/', null=True, blank=True)  # For uploading documents like PDFs
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.patient.username}"
