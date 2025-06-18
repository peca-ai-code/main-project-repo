from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from utils.availability_services import availability_service
from utils.appointment_services import appointment_service
from datetime import datetime, date
from typing import List  # Added this import

@api_view(['GET'])
@permission_classes([AllowAny])
def get_doctor_availability_calendar(request, doctor_id):
    """Get comprehensive availability calendar for a doctor"""
    try:
        weeks = int(request.GET.get('weeks', 4))  # Default 4 weeks
        weeks = min(weeks, 8)  # Max 8 weeks
        
        availability_data = availability_service.get_doctor_availability_calendar(doctor_id, weeks)
        
        if 'error' in availability_data:
            return Response(availability_data, status=status.HTTP_404_NOT_FOUND)
        
        return Response(availability_data)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch availability calendar: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET']) 
@permission_classes([AllowAny])
def check_slot_availability(request, doctor_id):
    """Check real-time availability of specific slot"""
    try:
        appointment_date_str = request.GET.get('date')
        time_slot = request.GET.get('time')
        
        if not appointment_date_str or not time_slot:
            return Response(
                {'error': 'Date and time parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%d').date()
        slot_status = availability_service.get_slot_availability_status(
            doctor_id, appointment_date, time_slot
        )
        
        return Response(slot_status)
        
    except ValueError:
        return Response(
            {'error': 'Invalid date format. Use YYYY-MM-DD'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Failed to check slot availability: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_availability_summary(request, doctor_id):
    """Get quick availability summary for a doctor"""
    try:
        availability_data = availability_service.get_doctor_availability_calendar(doctor_id, weeks=2)
        
        if 'error' in availability_data:
            return Response(availability_data, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'doctor_id': doctor_id,
            'summary': availability_data['summary'],
            'next_available_dates': get_next_available_dates(doctor_id, 5)
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch availability summary: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Helper function for next available dates
def get_next_available_dates(doctor_id: str, count: int = 5) -> List[str]:
    """Get next N available dates"""
    availability_data = availability_service.get_doctor_availability_calendar(doctor_id, weeks=4)
    if 'error' in availability_data:
        return []
    
    available_dates = []
    for date_str, date_info in availability_data['calendar'].items():
        if date_info['status'] in ['available', 'limited'] and date_info['available_count'] > 0:
            available_dates.append(date_str)
            if len(available_dates) >= count:
                break
    
    return available_dates

# Add this method to AvailabilityService class
from utils.availability_services import AvailabilityService
AvailabilityService.get_next_available_dates = staticmethod(get_next_available_dates)
