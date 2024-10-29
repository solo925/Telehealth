from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import DoctorProfile, PatientProfile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import DoctorProfile, PatientProfile

User = get_user_model()
class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['id', 'user', 'profile_picture', 'department', 'bio']

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['id', 'user', 'profile_picture', 'address', 'physical_address', 'blood_group', 'age']


class UserSerializer(serializers.ModelSerializer):
    doctor_profile = DoctorProfileSerializer(required=False)
    patient_profile = PatientProfileSerializer(required=False)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'is_doctor', 'is_patient', 'doctor_profile', 'patient_profile']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        doctor_data = validated_data.pop('doctor_profile', None)
        patient_data = validated_data.pop('patient_profile', None)
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            is_doctor=validated_data.get('is_doctor', False),
            is_patient=validated_data.get('is_patient', False)
        )
        if doctor_data:
            DoctorProfile.objects.create(user=user, **doctor_data)
        if patient_data:
            PatientProfile.objects.create(user=user, **patient_data)
        return user
