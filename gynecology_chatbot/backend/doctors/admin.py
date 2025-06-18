from django.contrib import admin
from .models import Doctor, Appointment, PatientQuery

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'specialty', 'experience_years', 'rating', 'status']
    list_filter = ['specialty', 'status']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['appointment_id', 'doctor', 'patient_display_name', 'appointment_date', 'status']
    list_filter = ['status', 'appointment_date']
    search_fields = ['patient_name', 'patient_email']

@admin.register(PatientQuery)
class PatientQueryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'severity_score', 'doctor_reviewed', 'created_at']
    list_filter = ['severity_score', 'doctor_reviewed']
    search_fields = ['patient__username', 'query_text']
