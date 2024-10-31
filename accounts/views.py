from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import DoctorProfile, PatientProfile
from accounts.models import User
from .serializers import DoctorProfileSerializer, PatientProfileSerializer, UserSerializer
from accounts.decorators import role_required
from rest_framework import generics


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = request.data
        serializer = UserSerializer(data=user_data)

        if serializer.is_valid():
            user = serializer.save()  # Save User model

            # Depending on the role, create DoctorProfile or PatientProfile
            role = user_data.get('role')
            if role == 'Doctor':
                doctor_profile_data = {
                    'user': user.id,
                    'department': user_data.get('department'),
                    # Add any other required fields for DoctorProfile here
                }
                doctor_serializer = DoctorProfileSerializer(data=doctor_profile_data)
                if doctor_serializer.is_valid():
                    doctor_serializer.save()
            elif role == 'Patient':
                patient_profile_data = {
                    'user': user.id,
                    'blood_group': user_data.get('blood_group'),
                    'age': user_data.get('age'),
                    'profile_picture': user_data.get('profile_picture'),
                    'firstname': user_data.get('firstname'),
                    'middlename': user_data.get('middlename'),
                    'surname': user_data.get('surname'),
                    'address': user_data.get('address'),
                    'physical_address': user_data.get('physical_address'),
                }
            
                patient_serializer = PatientProfileSerializer(data=patient_profile_data)
                if patient_serializer.is_valid():
                    patient_serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = RefreshToken.for_user(user)
            role = user.role
            dashboard_url = 'doctor_dashboard' if role == 'Doctor' else 'patient_dashboard'
            
            return Response({
                'refresh': str(token),
                'access': str(token.access_token),
                'role': role,
                'dashboard_url': dashboard_url
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



@role_required('Doctor')
class DoctorProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):     
        return get_object_or_404(DoctorProfile, user=self.request.user)

@role_required('Patient')
class PatientProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(PatientProfile, user=self.request.user)

