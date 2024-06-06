from django.db import models
from users.models import User

class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

class Availability(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_doctor': True}, related_name='availabilities')
    date = models.DateField()
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

class Appointment(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_doctor': True}, related_name='doctor_appointments')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_patient': True}, related_name='patient_appointments')
    date = models.DateField()
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    is_canceled = models.BooleanField(default=False)

class Waitlist(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='waitlist')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_patient': True})
    created_at = models.DateTimeField(auto_now_add=True)
