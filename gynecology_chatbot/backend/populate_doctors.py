import os
import django
from datetime import date, time, timedelta
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gynecology_chatbot_project.settings')
django.setup()

from utils.firestore_client import firestore_client

def create_doctors():
    """Create real doctor data in Firestore"""
    doctors_data = [
        {
            'name': 'Dr. Priya Sharma',
            'email': 'priya.sharma@womancaretech.com',
            'qualification': 'MBBS, MD (Obstetrics & Gynecology), AIIMS Delhi',
            'specialty': 'General Gynecology',
            'experience_years': 12,
            'consultation_fee': 1800,
            'rating': 4.8,
            'phone': '+91-9876543210',
            'clinic_name': 'Delhi Women\'s Health Center',
            'clinic_address': 'Connaught Place, New Delhi',
            'languages': ['English', 'Hindi', 'Punjabi'],
            'working_hours': {
                'monday': {'start': '09:00', 'end': '17:00'},
                'tuesday': {'start': '09:00', 'end': '17:00'},
                'wednesday': {'start': '09:00', 'end': '17:00'},
                'thursday': {'start': '09:00', 'end': '17:00'},
                'friday': {'start': '09:00', 'end': '17:00'},
                'saturday': {'start': '09:00', 'end': '13:00'},
                'sunday': {'closed': True}
            },
            'bio': 'Specialized in women\'s reproductive health with 12+ years of experience.',
            'is_available': True,
            'is_accepting_new_patients': True
        },
        {
            'name': 'Dr. Anjali Desai',
            'email': 'anjali.desai@womancaretech.com',
            'qualification': 'MBBS, DNB (Obstetrics & Gynecology)',
            'specialty': 'Obstetrics & Gynecology',
            'experience_years': 15,
            'consultation_fee': 2000,
            'rating': 4.9,
            'phone': '+91-9876543211',
            'clinic_name': 'Mumbai Maternity Center',
            'clinic_address': 'Bandra West, Mumbai',
            'languages': ['English', 'Hindi', 'Marathi'],
            'working_hours': {
                'monday': {'start': '10:00', 'end': '18:00'},
                'tuesday': {'start': '10:00', 'end': '18:00'},
                'wednesday': {'start': '10:00', 'end': '18:00'},
                'thursday': {'start': '10:00', 'end': '18:00'},
                'friday': {'start': '10:00', 'end': '18:00'},
                'saturday': {'start': '10:00', 'end': '14:00'},
                'sunday': {'closed': True}
            },
            'bio': 'Expert in high-risk pregnancies and minimally invasive gynecological procedures.',
            'is_available': True,
            'is_accepting_new_patients': True
        },
        {
            'name': 'Dr. Sarika Patel',
            'email': 'sarika.patel@womancaretech.com',
            'qualification': 'MBBS, MS (Obstetrics & Gynecology), PGIMER',
            'specialty': 'Fertility Specialist',
            'experience_years': 10,
            'consultation_fee': 2200,
            'rating': 4.7,
            'phone': '+91-9876543212',
            'clinic_name': 'Bangalore Fertility Clinic',
            'clinic_address': 'Koramangala, Bangalore',
            'languages': ['English', 'Hindi', 'Kannada'],
            'working_hours': {
                'monday': {'start': '08:00', 'end': '16:00'},
                'tuesday': {'start': '08:00', 'end': '16:00'},
                'wednesday': {'start': '08:00', 'end': '16:00'},
                'thursday': {'start': '08:00', 'end': '16:00'},
                'friday': {'start': '08:00', 'end': '16:00'},
                'saturday': {'start': '08:00', 'end': '12:00'},
                'sunday': {'closed': True}
            },
            'bio': 'Specialist in IVF, IUI, and reproductive endocrinology.',
            'is_available': True,
            'is_accepting_new_patients': True
        },
        {
            'name': 'Dr. Kavita Singh',
            'email': 'kavita.singh@womancaretech.com',
            'qualification': 'MBBS, MD (Obstetrics & Gynecology), AIIMS',
            'specialty': 'Gynecologic Oncology',
            'experience_years': 20,
            'consultation_fee': 2500,
            'rating': 4.9,
            'phone': '+91-9876543213',
            'clinic_name': 'Chennai Cancer Care Center',
            'clinic_address': 'T. Nagar, Chennai',
            'languages': ['English', 'Hindi', 'Tamil'],
            'working_hours': {
                'monday': {'start': '09:00', 'end': '17:00'},
                'tuesday': {'start': '09:00', 'end': '17:00'},
                'wednesday': {'start': '09:00', 'end': '17:00'},
                'thursday': {'start': '09:00', 'end': '17:00'},
                'friday': {'start': '09:00', 'end': '17:00'},
                'saturday': {'closed': True},
                'sunday': {'closed': True}
            },
            'bio': 'Leading expert in gynecological cancers and minimally invasive surgery.',
            'is_available': True,
            'is_accepting_new_patients': True
        },
        {
            'name': 'Dr. Meera Reddy',
            'email': 'meera.reddy@womancaretech.com',
            'qualification': 'MBBS, DGO (Obstetrics & Gynecology)',
            'specialty': 'General Gynecology',
            'experience_years': 7,
            'consultation_fee': 1500,
            'rating': 4.5,
            'phone': '+91-9876543214',
            'clinic_name': 'Hyderabad Women\'s Clinic',
            'clinic_address': 'Banjara Hills, Hyderabad',
            'languages': ['English', 'Hindi', 'Telugu'],
            'working_hours': {
                'monday': {'start': '09:00', 'end': '17:00'},
                'tuesday': {'start': '09:00', 'end': '17:00'},
                'wednesday': {'start': '09:00', 'end': '17:00'},
                'thursday': {'start': '09:00', 'end': '17:00'},
                'friday': {'start': '09:00', 'end': '17:00'},
                'saturday': {'start': '09:00', 'end': '13:00'},
                'sunday': {'closed': True}
            },
            'bio': 'Young and enthusiastic gynecologist with focus on adolescent health.',
            'is_available': True,
            'is_accepting_new_patients': True
        }
    ]
    
    print("Creating doctors in Firestore...")
    for i, doctor_data in enumerate(doctors_data, 1):
        # Add additional fields
        doctor_data.update({
            'doctor_id': f'DOC_{i:03d}',
            'total_consultations': 50 + i * 10,
            'created_at': date.today(),
            'status': 'active'
        })
        
        doc_id = firestore_client.create_document('doctors', doctor_data)
        print(f"✅ Created doctor: {doctor_data['name']} (ID: {doc_id})")
    
    print(f"\n✅ Successfully created {len(doctors_data)} doctors in Firestore!")

if __name__ == "__main__":
    create_doctors()
