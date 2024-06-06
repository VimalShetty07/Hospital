from django.urls import path
from .views import UserCreateView, DoctorProfileCreateView, PatientProfileCreateView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('doctor-profile/', DoctorProfileCreateView.as_view(), name='doctor-profile'),
    path('patient-profile/', PatientProfileCreateView.as_view(), name='patient-profile'),
]
