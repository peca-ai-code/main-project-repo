from typing import Dict, List, Any, Optional
from datetime import datetime, date, time, timedelta
from utils.firestore_client import firestore_client
import uuid

class AppointmentService:
    """Service for managing appointments in Firestore"""
    
    @staticmethod
    def get_available_doctors(specialty: str = None, location: str = None) -> List[Dict[str, Any]]:
        """Get list of available doctors with optional filters"""
        filters = [('is_available', '==', True), ('is_accepting_new_patients', '==', True)]
        
        if specialty:
            filters.append(('specialty', '==', specialty))
        
        doctors = firestore_client.query_collection('doctors', filters=filters)
        return doctors
    
    @staticmethod
    def get_doctor_by_id(doctor_id: str) -> Optional[Dict[str, Any]]:
        """Get doctor details by ID"""
        return firestore_client.get_document('doctors', doctor_id)
    
    @staticmethod
    def get_available_slots(doctor_id: str, appointment_date: date) -> List[str]:
        """Get available time slots for a doctor on a specific date"""
        doctor = AppointmentService.get_doctor_by_id(doctor_id)
        if not doctor:
            return []
        
        # Get day of week
        day_name = appointment_date.strftime('%A').lower()
        working_hours = doctor.get('working_hours', {}).get(day_name, {})
        
        if working_hours.get('closed', False):
            return []
        
        # Generate time slots
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
        
        # Remove booked slots
        booked_slots = AppointmentService.get_booked_slots(doctor_id, appointment_date)
        available_slots = [slot for slot in slots if slot not in booked_slots]
        
        return available_slots
    
    @staticmethod
    def get_booked_slots(doctor_id: str, appointment_date: date) -> List[str]:
        """Get booked time slots for a doctor on a specific date"""
        # Convert date to string for Firestore query
        date_str = appointment_date.strftime('%Y-%m-%d')
        
        filters = [
            ('doctor_id', '==', doctor_id),
            ('appointment_date', '==', date_str),  # Use string instead of date object
            ('status', 'in', ['pending', 'confirmed'])
        ]
        
        appointments = firestore_client.query_collection('appointments', filters=filters)
        return [app.get('appointment_time') for app in appointments]
    
    @staticmethod
    def create_appointment(appointment_data: Dict[str, Any]) -> str:
        """Create a new appointment"""
        # Convert date object to string if present
        if 'appointment_date' in appointment_data and isinstance(appointment_data['appointment_date'], date):
            appointment_data['appointment_date'] = appointment_data['appointment_date'].strftime('%Y-%m-%d')
        
        # Add appointment ID and timestamps
        appointment_data.update({
            'appointment_id': str(uuid.uuid4()),
            'status': 'pending',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        })
        
        return firestore_client.create_document('appointments', appointment_data)
    
    @staticmethod
    def get_user_appointments(user_id: str) -> List[Dict[str, Any]]:
        """Get all appointments for a user"""
        filters = [('patient_id', '==', user_id)]
        appointments = firestore_client.query_collection(
            'appointments', 
            filters=filters, 
            order_by='appointment_date'
        )
        
        # Enrich with doctor information
        for appointment in appointments:
            doctor = AppointmentService.get_doctor_by_id(appointment.get('doctor_id'))
            if doctor:
                appointment['doctor_name'] = doctor.get('name')
                appointment['doctor_specialty'] = doctor.get('specialty')
                appointment['clinic_name'] = doctor.get('clinic_name')
        
        return appointments
    
    @staticmethod
    def update_appointment_status(appointment_id: str, status: str, notes: str = '') -> bool:
        """Update appointment status"""
        # Find appointment by appointment_id
        appointments = firestore_client.query_collection(
            'appointments',
            filters=[('appointment_id', '==', appointment_id)]
        )
        
        if appointments:
            appointment = appointments[0]
            update_data = {
                'status': status,
                'updated_at': datetime.now()
            }
            if notes:
                update_data['notes'] = notes
            
            return firestore_client.update_document('appointments', appointment['id'], update_data)
        
        return False
    
    @staticmethod
    def get_specialties() -> List[str]:
        """Get all available specialties"""
        doctors = firestore_client.query_collection('doctors')
        specialties = list(set(doctor.get('specialty', '') for doctor in doctors))
        return [s for s in specialties if s]  # Remove empty strings

# Global service instance
appointment_service = AppointmentService()
