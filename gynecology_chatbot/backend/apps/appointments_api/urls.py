from django.urls import path
from . import views
from .availability_views import (
    get_doctor_availability_calendar, 
    check_slot_availability,
    get_availability_summary
)

urlpatterns = [
    # Doctor endpoints
    path('doctors/', views.get_doctors, name='get-doctors'),
    path('doctors/<str:doctor_id>/', views.get_doctor_details, name='get-doctor-details'),
    path('doctors/<str:doctor_id>/slots/', views.get_available_slots, name='get-available-slots'),
    
    # Appointment endpoints
    path('book/', views.book_appointment, name='book-appointment'),
    path('my-appointments/', views.get_my_appointments, name='get-my-appointments'),
    
    # Utility endpoints
    path('specialties/', views.get_specialties, name='get-specialties'),
    path('health/', views.appointment_health, name='appointment-health'),
    
    # Availability endpoints
    path('doctors/<str:doctor_id>/availability/', get_doctor_availability_calendar, name='doctor-availability-calendar'),
    path('doctors/<str:doctor_id>/availability/check/', check_slot_availability, name='check-slot-availability'),
    path('doctors/<str:doctor_id>/availability/summary/', get_availability_summary, name='availability-summary'),
]
