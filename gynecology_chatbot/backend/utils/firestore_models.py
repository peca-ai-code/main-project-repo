from typing import Dict, List, Any, Optional
from datetime import datetime, date, time
from utils.firestore_client import firestore_client
import uuid
from google.cloud import firestore

class FirestoreBaseModel:
    """Base class for Firestore models"""
    collection_name = None
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary"""
        data = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_') and key != 'id':
                if isinstance(value, (datetime, date, time)):
                    data[key] = value
                elif isinstance(value, uuid.UUID):
                    data[key] = str(value)
                else:
                    data[key] = value
        return data
    
    def save(self) -> str:
        """Save the model to Firestore"""
        data = self.to_dict()
        if self.id:
            firestore_client.update_document(self.collection_name, self.id, data)
            return self.id
        else:
            doc_id = firestore_client.create_document(self.collection_name, data)
            self.id = doc_id
            return doc_id
    
    def delete(self) -> bool:
        """Delete the model from Firestore"""
        if self.id:
            return firestore_client.delete_document(self.collection_name, self.id)
        return False
    
    @classmethod
    def get(cls, doc_id: str):
        """Get a model instance by ID"""
        data = firestore_client.get_document(cls.collection_name, doc_id)
        if data:
            return cls(**data)
        return None
    
    @classmethod
    def filter(cls, filters: List = None, order_by: str = None, limit: int = None):
        """Filter model instances"""
        data_list = firestore_client.query_collection(
            cls.collection_name, filters, order_by, limit
        )
        return [cls(**data) for data in data_list]

class FirestoreUser(FirestoreBaseModel):
    collection_name = 'users'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = kwargs.get('username', '')
        self.email = kwargs.get('email', '')
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        self.date_of_birth = kwargs.get('date_of_birth')
        self.has_accepted_terms = kwargs.get('has_accepted_terms', False)
        self.preferred_model = kwargs.get('preferred_model', 'openai')
        self.show_all_models = kwargs.get('show_all_models', True)
        self.is_active = kwargs.get('is_active', True)
        self.is_staff = kwargs.get('is_staff', False)
        self.password_hash = kwargs.get('password_hash', '')
    
    @classmethod
    def get_by_email(cls, email: str):
        """Get user by email"""
        results = cls.filter(filters=[('email', '==', email)])
        return results[0] if results else None
    
    @classmethod
    def get_by_username(cls, username: str):
        """Get user by username"""
        results = cls.filter(filters=[('username', '==', username)])
        return results[0] if results else None

class FirestoreConversation(FirestoreBaseModel):
    collection_name = 'conversations'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = kwargs.get('user_id', '')
        self.title = kwargs.get('title', 'New Conversation')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
    
    @classmethod
    def get_by_user(cls, user_id: str):
        """Get conversations by user ID"""
        return cls.filter(
            filters=[('user_id', '==', user_id)],
            order_by='updated_at',
            limit=50
        )

class FirestoreMessage(FirestoreBaseModel):
    collection_name = 'messages'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conversation_id = kwargs.get('conversation_id', '')
        self.content = kwargs.get('content', '')
        self.message_type = kwargs.get('message_type', 'user')  # user, assistant, system
        self.model_name = kwargs.get('model_name', '')
        self.metadata = kwargs.get('metadata', {})
        self.created_at = kwargs.get('created_at')

class FirestoreDoctor(FirestoreBaseModel):
    collection_name = 'doctors'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = kwargs.get('user_id', '')
        self.license_number = kwargs.get('license_number', '')
        self.specialty = kwargs.get('specialty', '')
        self.qualification = kwargs.get('qualification', '')
        self.experience_years = kwargs.get('experience_years', 0)
        self.clinic_name = kwargs.get('clinic_name', '')
        self.clinic_address = kwargs.get('clinic_address', '')
        self.phone_number = kwargs.get('phone_number', '')
        self.consultation_fee = kwargs.get('consultation_fee', 1500.0)
        self.rating = kwargs.get('rating', 4.0)
        self.total_consultations = kwargs.get('total_consultations', 0)
        self.status = kwargs.get('status', 'active')
        self.is_available_online = kwargs.get('is_available_online', True)
        self.is_accepting_new_patients = kwargs.get('is_accepting_new_patients', True)
        self.bio = kwargs.get('bio', '')
        self.languages_spoken = kwargs.get('languages_spoken', 'English, Hindi')
        self.last_active = kwargs.get('last_active')
    
    @classmethod
    def get_by_user_id(cls, user_id: str):
        """Get doctor by user ID"""
        results = cls.filter(filters=[('user_id', '==', user_id)])
        return results[0] if results else None

class FirestoreAppointment(FirestoreBaseModel):
    collection_name = 'appointments'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.appointment_id = kwargs.get('appointment_id', str(uuid.uuid4()))
        self.doctor_id = kwargs.get('doctor_id', '')
        self.patient_id = kwargs.get('patient_id', '')
        self.patient_name = kwargs.get('patient_name', '')
        self.patient_email = kwargs.get('patient_email', '')
        self.patient_phone = kwargs.get('patient_phone', '')
        self.patient_age = kwargs.get('patient_age')
        self.appointment_date = kwargs.get('appointment_date')
        self.appointment_time = kwargs.get('appointment_time')
        self.duration_minutes = kwargs.get('duration_minutes', 30)
        self.appointment_type = kwargs.get('appointment_type', 'consultation')
        self.status = kwargs.get('status', 'pending')
        self.reason_for_visit = kwargs.get('reason_for_visit', '')
        self.doctor_notes = kwargs.get('doctor_notes', '')
        self.patient_notes = kwargs.get('patient_notes', '')
        self.consultation_fee = kwargs.get('consultation_fee', 1500.0)
        self.payment_status = kwargs.get('payment_status', 'pending')
        self.related_conversation_id = kwargs.get('related_conversation_id', '')
    
    @classmethod
    def get_by_doctor(cls, doctor_id: str):
        """Get appointments by doctor ID"""
        return cls.filter(
            filters=[('doctor_id', '==', doctor_id)],
            order_by='appointment_date'
        )

class FirestorePatientQuery(FirestoreBaseModel):
    collection_name = 'patient_queries'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.patient_id = kwargs.get('patient_id', '')
        self.conversation_id = kwargs.get('conversation_id', '')
        self.assigned_doctor_id = kwargs.get('assigned_doctor_id', '')
        self.query_text = kwargs.get('query_text', '')
        self.ai_response = kwargs.get('ai_response', '')
        self.severity_score = kwargs.get('severity_score', 3)
        self.doctor_reviewed = kwargs.get('doctor_reviewed', False)
        self.doctor_response = kwargs.get('doctor_response', '')
        self.doctor_recommendation = kwargs.get('doctor_recommendation', '')
        self.requires_appointment = kwargs.get('requires_appointment', False)
        self.reviewed_at = kwargs.get('reviewed_at')
