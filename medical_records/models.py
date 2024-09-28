"""
Defines the `MedicalRecord` model, which represents a medical record for a patient.

The `MedicalRecord` model has the following fields:
- `doctor`: A foreign key to the `User` model, representing the doctor who created the record.
- `patient`: A foreign key to the `User` model, representing the patient the record belongs to.
- `title`: A character field for the title of the medical record.
- `description`: A text field for the description of the medical record.
- `document`: An optional file field for uploading documents related to the medical record.
- `created_at`: A datetime field that automatically records the time the record was created.

The `__str__` method returns a string representation of the medical record, showing the title and the patient's username.
"""
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
