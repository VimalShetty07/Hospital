from rest_framework import generics
from .models import User, DoctorProfile, PatientProfile
from .serializers import UserSerializer, DoctorProfileSerializer, PatientProfileSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DoctorProfileCreateView(generics.CreateAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer

class PatientProfileCreateView(generics.CreateAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
