from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date, time, timedelta
from utils.firestore_client import firestore_client
from utils.appointment_services import AppointmentService
import calendar

class AvailabilityService:
    """Advanced service for managing real-time doctor availability"""
    
    @staticmethod
    def get_doctor_availability_calendar(doctor_id: str, weeks: int = 4) -> Dict[str, Any]:
        """Get comprehensive availability calendar for a doctor"""
        doctor = AppointmentService.get_doctor_by_id(doctor_id)
        if not doctor:
            return {"error": "Doctor not found"}
        
        # Generate date range
        start_date = date.today() + timedelta(days=1)  # Start from tomorrow
        end_date = start_date + timedelta(weeks=weeks * 7)
        
        availability_calendar = {}
        date_range = []
        
        current_date = start_date
        while current_date <= end_date:
            date_range.append(current_date)
            current_date += timedelta(days=1)
        
        for check_date in date_range:
            date_str = check_date.strftime('%Y-%m-%d')
            day_name = check_date.strftime('%A').lower()
            
            # Check if doctor works on this day
            working_hours = doctor.get('working_hours', {}).get(day_name, {})
            
            if working_hours.get('closed', False):
                availability_calendar[date_str] = {
                    'status': 'closed',
                    'available_slots': [],
                    'booked_slots': [],
                    'total_slots': 0,
                    'available_count': 0,
                    'day_name': check_date.strftime('%A')
                }
            else:
                # Get all possible slots for the day
                all_slots = AvailabilityService._generate_day_slots(working_hours)
                booked_slots = AppointmentService.get_booked_slots(doctor_id, check_date)
                available_slots = [slot for slot in all_slots if slot not in booked_slots]
                
                # Determine day status
                if len(available_slots) == 0:
                    day_status = 'fully_booked'
                elif len(available_slots) <= len(all_slots) * 0.2:  # Less than 20% available
                    day_status = 'limited'
                else:
                    day_status = 'available'
                
                availability_calendar[date_str] = {
                    'status': day_status,
                    'available_slots': available_slots,
                    'booked_slots': booked_slots,
                    'total_slots': len(all_slots),
                    'available_count': len(available_slots),
                    'day_name': check_date.strftime('%A'),
                    'working_hours': working_hours
                }
        
        return {
            'doctor_id': doctor_id,
            'doctor_name': doctor.get('name', 'Unknown'),
            'calendar': availability_calendar,
            'summary': AvailabilityService._generate_availability_summary(availability_calendar)
        }
    
    @staticmethod
    def _generate_day_slots(working_hours: Dict[str, str]) -> List[str]:
        """Generate all possible time slots for a day"""
        start_time = working_hours.get('start', '09:00')
        end_time = working_hours.get('end', '17:00')
        
        slots = []
        current_time = datetime.strptime(start_time, '%H:%M').time()
        end_time_obj = datetime.strptime(end_time, '%H:%M').time()
        
        while current_time < end_time_obj:
            slots.append(current_time.strftime('%H:%M'))
            # Add 30 minutes
            current_datetime = datetime.combine(date.today(), current_time)
            current_datetime += timedelta(minutes=30)
            current_time = current_datetime.time()
        
        return slots
    
    @staticmethod
    def _generate_availability_summary(calendar: Dict[str, Any]) -> Dict[str, int]:
        """Generate summary statistics for availability calendar"""
        summary = {
            'total_days': len(calendar),
            'available_days': 0,
            'limited_days': 0,
            'fully_booked_days': 0,
            'closed_days': 0,
            'total_available_slots': 0
        }
        
        for date_info in calendar.values():
            status = date_info['status']
            if status == 'available':
                summary['available_days'] += 1
            elif status == 'limited':
                summary['limited_days'] += 1
            elif status == 'fully_booked':
                summary['fully_booked_days'] += 1
            elif status == 'closed':
                summary['closed_days'] += 1
            
            summary['total_available_slots'] += date_info.get('available_count', 0)
        
        return summary
    
    @staticmethod  
    def get_slot_availability_status(doctor_id: str, appointment_date: date, time_slot: str) -> Dict[str, Any]:
        """Check if a specific slot is available and get detailed status"""
        try:
            # Get booked slots for the date
            booked_slots = AppointmentService.get_booked_slots(doctor_id, appointment_date)
            
            # Check if slot is booked
            is_available = time_slot not in booked_slots
            
            # Get recent booking activity (last 5 minutes)
            recent_bookings = AvailabilityService._get_recent_bookings(doctor_id, appointment_date)
            recently_booked = any(booking['appointment_time'] == time_slot for booking in recent_bookings)
            
            return {
                'available': is_available,
                'recently_booked': recently_booked,
                'slot_time': time_slot,
                'date': appointment_date.strftime('%Y-%m-%d'),
                'total_booked_slots': len(booked_slots),
                'booking_pressure': 'high' if len(booked_slots) > 10 else 'normal'
            }
            
        except Exception as e:
            return {
                'available': False,
                'error': str(e),
                'slot_time': time_slot,
                'date': appointment_date.strftime('%Y-%m-%d')
            }
    
    @staticmethod
    def _get_recent_bookings(doctor_id: str, appointment_date: date) -> List[Dict[str, Any]]:
        """Get appointments booked in the last 5 minutes for real-time updates"""
        date_str = appointment_date.strftime('%Y-%m-%d')
        five_minutes_ago = datetime.now() - timedelta(minutes=5)
        
        filters = [
            ('doctor_id', '==', doctor_id),
            ('appointment_date', '==', date_str),
            ('status', '==', 'pending')
        ]
        
        appointments = firestore_client.query_collection('appointments', filters=filters)
        
        # Filter by creation time (last 5 minutes)
        recent = []
        for appointment in appointments:
            created_at = appointment.get('created_at')
            if created_at and created_at > five_minutes_ago:
                recent.append(appointment)
        
        return recent

# Global service instance
availability_service = AvailabilityService()
