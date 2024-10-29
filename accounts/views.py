from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from .models import DoctorProfile, PatientProfile
from accounts.models import User
from .serializers import DoctorProfileSerializer, PatientProfileSerializer,UserSerializer
from django.shortcuts import get_object_or_404
from accounts.decorators import role_required


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
            return Response({
                'refresh': str(token),
                'access': str(token.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



@role_required('Doctor')
class DoctorProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(DoctorProfile, user=self.request.user)

@role_required('patient')
class PatientProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(PatientProfile, user=self.request.user)
