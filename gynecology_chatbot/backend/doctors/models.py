from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.chatbot.models import Conversation, Message
import uuid

User = get_user_model()

class Doctor(models.Model):
    SPECIALTIES = [
        ('general_gynecology', 'General Gynecology'),
        ('obstetrics_gynecology', 'Obstetrics & Gynecology'),
        ('fertility_specialist', 'Fertility Specialist'),
        ('gynecologic_oncology', 'Gynecologic Oncology'),
        ('maternal_fetal_medicine', 'Maternal-Fetal Medicine'),
        ('reproductive_endocrinology', 'Reproductive Endocrinology'),
        ('urogynecology', 'Urogynecology'),
        ('pediatric_adolescent_gynecology', 'Pediatric & Adolescent Gynecology'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_leave', 'On Leave'),
        ('busy', 'Busy'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    license_number = models.CharField(max_length=50, unique=True)
    specialty = models.CharField(max_length=50, choices=SPECIALTIES)
    qualification = models.TextField()
    experience_years = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    
    clinic_name = models.CharField(max_length=200, blank=True)
    clinic_address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15)
    
    consultation_fee = models.DecimalField(max_digits=6, decimal_places=2, default=1500.00)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.0, 
                                validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_consultations = models.PositiveIntegerField(default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_available_online = models.BooleanField(default=True)
    is_accepting_new_patients = models.BooleanField(default=True)
    
    bio = models.TextField(blank=True)
    languages_spoken = models.CharField(max_length=200, default='English, Hindi')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-rating', '-experience_years']
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"
    
    @property
    def full_name(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"
    
    @property
    def initials(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name[0]}{self.user.last_name[0]}"
        return self.user.username[:2].upper()

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    TYPE_CHOICES = [
        ('consultation', 'General Consultation'),
        ('follow_up', 'Follow-up'),
        ('emergency', 'Emergency'),
        ('routine_checkup', 'Routine Checkup'),
    ]
    
    appointment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    
    patient_name = models.CharField(max_length=100, blank=True)
    patient_email = models.EmailField(blank=True)
    patient_phone = models.CharField(max_length=15, blank=True)
    patient_age = models.PositiveIntegerField(null=True, blank=True)
    
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    appointment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='consultation')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason_for_visit = models.TextField(blank=True)
    doctor_notes = models.TextField(blank=True)
    patient_notes = models.TextField(blank=True)
    
    consultation_fee = models.DecimalField(max_digits=6, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='pending')
    
    related_conversation = models.ForeignKey(Conversation, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
    
    def __str__(self):
        patient_name = self.patient.get_full_name() if self.patient else self.patient_name
        return f"{patient_name} - {self.doctor.full_name} - {self.appointment_date}"
    
    @property
    def patient_display_name(self):
        if self.patient:
            return self.patient.get_full_name() or self.patient.username
        return self.patient_name

class PatientQuery(models.Model):
    SEVERITY_CHOICES = [
        (1, 'Low - General Information'),
        (2, 'Low-Medium'),
        (3, 'Medium - Some Concern'),
        (4, 'Medium-High'),
        (5, 'High - Needs Attention'),
        (6, 'High-Medium'),
        (7, 'Very High - Urgent'),
        (8, 'Very High-Critical'),
        (9, 'Critical - Immediate Care'),
        (10, 'Emergency - Immediate Medical Attention'),
    ]
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queries')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='queries')
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_queries')
    
    query_text = models.TextField()
    ai_response = models.TextField()
    severity_score = models.IntegerField(choices=SEVERITY_CHOICES, default=3)
    
    doctor_reviewed = models.BooleanField(default=False)
    doctor_response = models.TextField(blank=True)
    doctor_recommendation = models.TextField(blank=True)
    requires_appointment = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-severity_score', '-created_at']
    
    def __str__(self):
        return f"{self.patient.username} - Severity {self.severity_score}"
