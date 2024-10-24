# urls.py
from django.urls import path
from .views import UploadMedicalRecordView, ViewMedicalRecordsView

app_name = "medical_records"

urlpatterns = [
    path('upload/', UploadMedicalRecordView.as_view(), name='upload_medical_record'),
    path('records/', ViewMedicalRecordsView.as_view(), name='view_medical_records'),
]
