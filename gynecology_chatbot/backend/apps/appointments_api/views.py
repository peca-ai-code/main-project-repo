from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from utils.appointment_services import appointment_service
from datetime import datetime, date
import json

@api_view(['GET'])
@permission_classes([AllowAny])
def get_doctors(request):
    """Get list of available doctors with optional filters"""
    specialty = request.GET.get('specialty')
    location = request.GET.get('location')
    
    try:
        doctors = appointment_service.get_available_doctors(specialty, location)
        
        # Format doctor data for frontend
        formatted_doctors = []
        for doctor in doctors:
            formatted_doctors.append({
                'id': doctor['id'],
                'name': doctor.get('name', ''),
                'specialty': doctor.get('specialty', ''),
                'qualification': doctor.get('qualification', ''),
                'experience_years': doctor.get('experience_years', 0),
                'rating': doctor.get('rating', 4.0),
                'consultation_fee': doctor.get('consultation_fee', 1500),
                'clinic_name': doctor.get('clinic_name', ''),
                'clinic_address': doctor.get('clinic_address', ''),
                'languages': doctor.get('languages', []),
                'bio': doctor.get('bio', ''),
                'phone': doctor.get('phone', ''),
                'initials': ''.join([word[0] for word in doctor.get('name', 'Dr').split()[-2:]])
            })
        
        return Response({
            'doctors': formatted_doctors,
            'count': len(formatted_doctors)
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch doctors: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_doctor_details(request, doctor_id):
    """Get detailed information about a specific doctor"""
    try:
        doctor = appointment_service.get_doctor_by_id(doctor_id)
        
        if not doctor:
            return Response(
                {'error': 'Doctor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'id': doctor['id'],
            'name': doctor.get('name', ''),
            'specialty': doctor.get('specialty', ''),
            'qualification': doctor.get('qualification', ''),
            'experience_years': doctor.get('experience_years', 0),
            'rating': doctor.get('rating', 4.0),
            'consultation_fee': doctor.get('consultation_fee', 1500),
            'clinic_name': doctor.get('clinic_name', ''),
            'clinic_address': doctor.get('clinic_address', ''),
            'languages': doctor.get('languages', []),
            'bio': doctor.get('bio', ''),
            'phone': doctor.get('phone', ''),
            'working_hours': doctor.get('working_hours', {}),
            'is_available': doctor.get('is_available', True)
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch doctor details: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_available_slots(request, doctor_id):
    """Get available time slots for a doctor on a specific date"""
    appointment_date_str = request.GET.get('date')
    
    if not appointment_date_str:
        return Response(
            {'error': 'Date parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%d').date()
        slots = appointment_service.get_available_slots(doctor_id, appointment_date)
        
        return Response({
            'date': appointment_date_str,
            'doctor_id': doctor_id,
            'available_slots': slots
        })
        
    except ValueError:
        return Response(
            {'error': 'Invalid date format. Use YYYY-MM-DD'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch available slots: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])  # Change to IsAuthenticated for production
def book_appointment(request):
    """Book a new appointment"""
    try:
        data = request.data
        
        # Validate required fields
        required_fields = ['doctor_id', 'appointment_date', 'appointment_time', 'patient_name', 'patient_email', 'patient_phone']
        for field in required_fields:
            if not data.get(field):
                return Response(
                    {'error': f'{field} is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Parse and validate date
        try:
            appointment_date = datetime.strptime(data['appointment_date'], '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if slot is still available
        available_slots = appointment_service.get_available_slots(data['doctor_id'], appointment_date)
        
        if data['appointment_time'] not in available_slots:
            return Response(
                {'error': 'Selected time slot is no longer available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get doctor details for consultation fee
        doctor = appointment_service.get_doctor_by_id(data['doctor_id'])
        if not doctor:
            return Response(
                {'error': 'Doctor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Prepare appointment data - store date as string
        appointment_data = {
            'doctor_id': data['doctor_id'],
            'patient_id': str(request.user.id) if request.user.is_authenticated else None,
            'patient_name': data['patient_name'],
            'patient_email': data['patient_email'],
            'patient_phone': data['patient_phone'],
            'patient_age': data.get('patient_age'),
            'appointment_date': data['appointment_date'],  # Keep as string
            'appointment_time': data['appointment_time'],
            'appointment_type': data.get('appointment_type', 'consultation'),
            'reason_for_visit': data.get('reason_for_visit', ''),
            'patient_notes': data.get('patient_notes', ''),
            'consultation_fee': doctor.get('consultation_fee', 1500),
            'doctor_name': doctor.get('name', ''),
            'clinic_name': doctor.get('clinic_name', ''),
            'specialty': doctor.get('specialty', '')
        }
        
        # Create appointment
        appointment_id = appointment_service.create_appointment(appointment_data)
        
        return Response({
            'success': True,
            'appointment_id': appointment_data['appointment_id'],
            'message': 'Appointment booked successfully',
            'appointment_details': {
                'doctor_name': doctor.get('name'),
                'date': data['appointment_date'],
                'time': data['appointment_time'],
                'clinic': doctor.get('clinic_name'),
                'fee': doctor.get('consultation_fee')
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to book appointment: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_appointments(request):
    """Get user's appointments"""
    try:
        user_id = str(request.user.id)
        appointments = appointment_service.get_user_appointments(user_id)
        
        return Response({
            'appointments': appointments,
            'count': len(appointments)
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch appointments: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_specialties(request):
    """Get all available specialties"""
    try:
        specialties = appointment_service.get_specialties()
        return Response({'specialties': specialties})
        
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch specialties: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def appointment_health(request):
    """Health check for appointment API"""
    return Response({
        'status': 'ok',
        'message': 'Appointment API is running',
        'timestamp': datetime.now().isoformat()
    })
