from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase
from .models import MedicalRecord

class MedicalRecordTests(APITestCase):
    def setUp(self):
    
        self.doctor = User.objects.create_user(username='doctor', password='password')
        self.doctor_group = Group.objects.create(name='Doctors')
        self.doctor.groups.add(self.doctor_group)
        
        self.patient = User.objects.create_user(username='patient', password='password')
        self.patient_group = Group.objects.create(name='Patients')
        self.patient.groups.add(self.patient_group)
     
        self.url = reverse('view_medical_records')
    
    def test_get_medical_records_for_doctor(self):
        self.client.force_authenticate(user=self.doctor)
        
        # Create medical records for the doctor
        MedicalRecord.objects.create(doctor=self.doctor, patient=User.objects.create_user(username='patient1'), description='Test record 1')
        MedicalRecord.objects.create(doctor=self.doctor, patient=User.objects.create_user(username='patient2'), description='Test record 2')
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['description'], 'Test record 1')
        self.assertEqual(response.data[1]['description'], 'Test record 2')
    
    def test_view_medical_records_empty_for_doctor(self):
        self.client.force_authenticate(user=self.doctor)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_view_medical_records_for_patient(self):
        self.client.force_authenticate(user=self.patient)
        
        # Create medical records for the patient
        MedicalRecord.objects.create(patient=self.patient, doctor=self.doctor, description='Test record 1')
        MedicalRecord.objects.create(patient=self.patient, doctor=self.doctor, description='Test record 2')
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['description'], 'Test record 1')
        self.assertEqual(response.data[1]['description'], 'Test record 2')
    
    def test_view_medical_records_empty_for_patient(self):
        self.client.force_authenticate(user=self.patient)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_view_medical_records_unauthenticated(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_view_medical_records_forbidden_for_admin(self):
        admin_user = User.objects.create_user(username='admin', password='adminpass')
        admin_group = Group.objects.create(name='Admin')
        admin_user.groups.add(admin_group)
        
        self.client.force_authenticate(user=admin_user)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_view_medical_records_pagination_for_doctor(self):
        self.client.force_authenticate(user=self.doctor)
        
        # Create 15 medical records
        for i in range(15):
            MedicalRecord.objects.create(doctor=self.doctor, patient=User.objects.create_user(username=f'patient{i}'), description=f'Diagnosis {i}')
        
        # First page should return 10 records by default
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        
        # Second page should return remaining 5 records
        response = self.client.get(response.data['next'])
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIsNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])
    
    def test_view_medical_records_pagination_for_patient(self):
        self.client.force_authenticate(user=self.patient)
        
        # Create 15 medical records for the patient
        for i in range(15):
            MedicalRecord.objects.create(patient=self.patient, doctor=self.doctor, description=f'Record {i}')
        
        response = self.client.get(self.url)
        
        # First page should return 10 records by default
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        
        # Second page should return remaining 5 records
        response = self.client.get(response.data['next'])
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIsNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])
    
    def test_view_medical_records_not_found(self):
        self.client.force_authenticate(user=self.doctor)
        
        # Ensure no medical records exist
        MedicalRecord.objects.all().delete()
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'No medical records found.'})
    
    def test_view_medical_records_invalid_pagination(self):
        self.client.force_authenticate(user=self.doctor)
        
        # Create some medical records
        for i in range(5):
            MedicalRecord.objects.create(doctor=self.doctor, patient=User.objects.create_user(username=f'patient{i}'), description=f'Record {i}')
        
        # Test invalid page size
        response = self.client.get(f"{self.url}?page_size=invalid")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test invalid page number
        response = self.client.get(f"{self.url}?page=invalid")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
