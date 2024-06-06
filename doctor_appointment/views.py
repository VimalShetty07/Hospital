from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from .models import TimeSlot, Availability, Appointment, Waitlist
from .serializers import TimeSlotSerializer, AvailabilitySerializer, AppointmentSerializer, WaitlistSerializer

class TimeSlotListView(generics.ListAPIView):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer

class AvailabilityCreateView(generics.CreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

class AppointmentCreateView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        slot_id = data['slot']
        date = data['date']
        patient_id = data['patient']

        # Ensure no double booking
        if Appointment.objects.filter(patient_id=patient_id, slot_id=slot_id, date=date, is_canceled=False).exists():
            return Response({"error": "You already have an appointment at this time."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

class AppointmentCancelView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_canceled = True
        instance.save()

        # Handle waitlist
        waitlist = instance.waitlist.filter().first()
        if waitlist:
            new_appointment = Appointment.objects.create(
                doctor=instance.doctor,
                patient=waitlist.patient,
                date=instance.date,
                slot=instance.slot,
                is_canceled=False
            )
            waitlist.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class AppointmentListView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        doctor_name = self.request.query_params.get('doctor_name')
        patient_name = self.request.query_params.get('patient_name')

        if doctor_name:
            queryset = queryset.filter(doctor__username__icontains=doctor_name)
        if patient_name:
            queryset = queryset.filter(patient__username__icontains=patient_name)

        return queryset
