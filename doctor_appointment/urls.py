from django.urls import path
from .views import TimeSlotListView, AvailabilityCreateView, AppointmentCreateView, AppointmentCancelView, AppointmentListView

urlpatterns = [
    path('timeslots/', TimeSlotListView.as_view(), name='timeslot-list'),
    path('availability/', AvailabilityCreateView.as_view(), name='availability-create'),
    path('appointments/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('appointments/<int:pk>/cancel/', AppointmentCancelView.as_view(), name='appointment-cancel'),
    path('appointments/search/', AppointmentListView.as_view(), name='appointment-search'),
]
