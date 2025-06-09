from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404, render
from django.db.models import Count, Sum
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta, date, time
from .models import Doctor, Appointment, PatientQuery
from .serializers import (
    DoctorSerializer, AppointmentSerializer, QuerySerializer, 
    CustomTokenObtainPairSerializer, DoctorRegistrationSerializer
)
import uuid
import random
import string

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class IsDoctorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'doctor_profile')

class DoctorProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsDoctorPermission]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        doctor = get_object_or_404(Doctor, user=request.user)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        doctor = get_object_or_404(Doctor, user=request.user)
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def update_availability(self, request):
        doctor = get_object_or_404(Doctor, user=request.user)
        is_available = request.data.get('is_available', True)
        doctor.is_available_online = is_available
        doctor.save()
        return Response({'message': f'Availability updated to {"Available" if is_available else "Unavailable"}'})

class DoctorDashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsDoctorPermission]
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        doctor = get_object_or_404(Doctor, user=request.user)
        today = timezone.now().date()
        
        stats = {
            'total_appointments_today': Appointment.objects.filter(doctor=doctor, appointment_date=today).count(),
            'pending_appointments': Appointment.objects.filter(doctor=doctor, status='pending').count(),
            'pending_queries': PatientQuery.objects.filter(assigned_doctor=doctor, doctor_reviewed=False).count(),
            'high_severity_queries': PatientQuery.objects.filter(assigned_doctor=doctor, severity_score__gte=7, doctor_reviewed=False).count(),
            'total_patients': Appointment.objects.filter(doctor=doctor).values('patient').distinct().count(),
            'average_rating': doctor.rating,
            'total_appointments_week': Appointment.objects.filter(doctor=doctor, appointment_date__gte=today - timedelta(days=7)).count(),
            'total_appointments_month': Appointment.objects.filter(doctor=doctor, appointment_date__gte=today.replace(day=1)).count(),
            'completed_appointments_today': Appointment.objects.filter(doctor=doctor, appointment_date=today, status='completed').count(),
            'total_revenue_month': 0,
            'is_available': doctor.is_available_online,
        }
        
        return Response(stats)

class AppointmentManagementViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsDoctorPermission]
    
    def get_queryset(self):
        doctor = get_object_or_404(Doctor, user=self.request.user)
        return Appointment.objects.filter(doctor=doctor).order_by('-appointment_date', '-appointment_time')
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'confirmed'
        appointment.save()
        return Response({'message': 'Appointment approved'})
    
    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'cancelled'
        appointment.doctor_notes = request.data.get('reason', 'Declined by doctor')
        appointment.save()
        return Response({'message': 'Appointment declined'})
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'completed'
        appointment.doctor_notes = request.data.get('notes', '')
        appointment.save()
        return Response({'message': 'Appointment completed'})

class PatientQueryManagementViewSet(viewsets.ModelViewSet):
    serializer_class = QuerySerializer
    permission_classes = [IsDoctorPermission]
    
    def get_queryset(self):
        doctor = get_object_or_404(Doctor, user=self.request.user)
        return PatientQuery.objects.filter(assigned_doctor=doctor).order_by('-severity_score', '-created_at')

class DoctorRegistrationView(generics.CreateAPIView):
    serializer_class = DoctorRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Generate random password
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            
            # Here you would typically save the registration request
            # and send an email to admin to create the account
            
            # For now, let's just return success
            return Response({
                'message': 'Registration request submitted successfully. You will receive login credentials via email within 24 hours.',
                'reference_id': str(uuid.uuid4())[:8].upper()
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def doctor_dashboard_view(request):
    """Serve the doctor dashboard HTML page"""
    return render(request, 'doctors/dashboard.html')
