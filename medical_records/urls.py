from django.urls import path
from . import views

app_name = "medical_records"
urlpatterns = [
    path('upload/', views.upload_medical_record, name='upload_medical_record'),
    path('records/', views.view_medical_records, name='view_medical_records'),
]
