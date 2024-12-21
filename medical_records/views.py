from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from rest_framework.permissions import IsAuthenticated

class UploadMedicalRecordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles the uploading of medical records by doctors.
        """
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save(doctor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewMedicalRecordsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handles viewing medical records by both doctors and patients.
        Doctors see the records they've created, patients see their own records.
        """
        if request.user.groups.filter(name='Doctors').exists():
       
            records = MedicalRecord.objects.filter(doctor=request.user)
        else:
          
            records = MedicalRecord.objects.filter(patient=request.user)

        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.parsers import MultiPartParser, FormParser

class UploadMedicalRecordView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  

    def post(self, request):
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(doctor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
