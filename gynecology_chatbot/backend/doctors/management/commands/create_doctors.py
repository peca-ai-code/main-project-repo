from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from doctors.models import Doctor, Appointment, PatientQuery
import random
from datetime import date, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample doctors and test data'
    
    def handle(self, *args, **options):
        # Create admin doctor
        username = 'dr.admin'
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email='dr.admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='Doctor'
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()
            
            doctor = Doctor.objects.create(
                user=user,
                license_number='MCI999999',
                specialty='general_gynecology',
                qualification='MBBS, MD (Obstetrics & Gynecology), AIIMS',
                experience_years=20,
                consultation_fee=2500.00,
                rating=5.0,
                phone_number='+919999999999',
                clinic_name='Admin Medical Center',
                clinic_address='Medical Complex, Delhi',
                bio='Administrative doctor account.',
                status='active',
                is_available_online=True,
                is_accepting_new_patients=True
            )
            
            # Create some sample appointments for the admin doctor
            guest_user = User.objects.filter(username='guest').first()
            if guest_user:
                for i in range(3):
                    Appointment.objects.create(
                        doctor=doctor,
                        patient=guest_user,
                        patient_name='Test Patient',
                        patient_email='test@example.com',
                        patient_phone='+919999999999',
                        appointment_date=date.today() + timedelta(days=i),
                        appointment_time='10:00',
                        consultation_fee=doctor.consultation_fee,
                        reason_for_visit='Regular checkup',
                        status='pending' if i == 0 else 'confirmed'
                    )
                
                # Create sample queries - with better error handling
                from apps.chatbot.models import Conversation
                try:
                    conversation = Conversation.objects.filter(user=guest_user).first()
                    if conversation:
                        for i in range(2):
                            PatientQuery.objects.create(
                                patient=guest_user,
                                conversation=conversation,
                                assigned_doctor=doctor,
                                query_text=f'Sample patient query {i+1} about gynecological health concerns',
                                ai_response=f'Sample AI response {i+1} providing general guidance',
                                severity_score=5 + i*2,
                                doctor_reviewed=False
                            )
                except Exception as e:
                    self.stdout.write(f'Note: Could not create sample queries: {e}')
            
            self.stdout.write(self.style.SUCCESS('Created admin doctor: dr.admin / admin123'))
        
        # Create sample doctors
        doctors_data = [
            {'name': 'Priya Sharma', 'specialty': 'general_gynecology', 'experience': 12, 'rating': 4.8, 'fee': 1800},
            {'name': 'Anjali Desai', 'specialty': 'obstetrics_gynecology', 'experience': 15, 'rating': 4.9, 'fee': 2000},
            {'name': 'Sarika Patel', 'specialty': 'fertility_specialist', 'experience': 10, 'rating': 4.7, 'fee': 2200},
        ]
        
        created_count = 0
        for doctor_data in doctors_data:
            name_parts = doctor_data['name'].lower().split()
            username = f"dr.{name_parts[0]}.{name_parts[1]}"
            
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f"{username}@example.com",
                    password='doctor123',
                    first_name=name_parts[0].title(),
                    last_name=name_parts[1].title()
                )
                
                Doctor.objects.create(
                    user=user,
                    license_number=f"MCI{random.randint(100000, 999999)}",
                    specialty=doctor_data['specialty'],
                    qualification='MBBS, MD (Obstetrics & Gynecology)',
                    experience_years=doctor_data['experience'],
                    consultation_fee=doctor_data['fee'],
                    rating=doctor_data['rating'],
                    phone_number=f"+91{random.randint(7000000000, 9999999999)}",
                    clinic_name=f"Dr. {doctor_data['name']} Clinic",
                    clinic_address=f"Sector {random.randint(1, 50)}, Delhi",
                    bio=f"Experienced {doctor_data['specialty'].replace('_', ' ')} specialist.",
                    status='active',
                    is_available_online=True,
                    is_accepting_new_patients=True
                )
                created_count += 1
                self.stdout.write(f'Created doctor: {doctor_data["name"]}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} sample doctors!'))
        self.stdout.write('Login credentials: username=dr.firstname.lastname, password=doctor123')
