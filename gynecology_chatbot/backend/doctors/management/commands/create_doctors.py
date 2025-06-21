from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from doctors.models import Doctor, Appointment, PatientQuery
import random
from datetime import date, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample doctors and test data'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🩺 Creating Doctor Accounts for WomanCare Dashboard'))
        self.stdout.write('=' * 60)
        
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
            
            self.stdout.write(self.style.SUCCESS('✅ Created admin doctor: dr.admin@example.com / admin123'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Admin doctor already exists'))
        
        # All doctors from appointment section with proper data
        doctors_data = [
            {
                'name': 'Priya Sharma', 
                'email': 'dr.priya.sharma@example.com',
                'specialty': 'general_gynecology', 
                'experience': 12, 
                'rating': 4.8, 
                'fee': 1800,
                'qualification': 'MBBS, MD (Obstetrics & Gynecology), AIIMS Delhi',
                'clinic': 'Sharma Women\'s Clinic',
                'address': 'Connaught Place, New Delhi',
                'phone': '+91-9876543210',
                'bio': 'Specialized in women\'s reproductive health with 12+ years of experience in general gynecology.'
            },
            {
                'name': 'Anjali Desai', 
                'email': 'dr.anjali.desai@example.com',
                'specialty': 'obstetrics_gynecology', 
                'experience': 15, 
                'rating': 4.9, 
                'fee': 2000,
                'qualification': 'MBBS, DNB (Obstetrics & Gynecology), Bombay Hospital',
                'clinic': 'Desai Maternity Center',
                'address': 'Bandra West, Mumbai',
                'phone': '+91-9876543211',
                'bio': 'Expert in high-risk pregnancies and minimally invasive gynecological procedures with 15+ years experience.'
            },
            {
                'name': 'Sarika Patel', 
                'email': 'dr.sarika.patel@example.com',
                'specialty': 'fertility_specialist', 
                'experience': 10, 
                'rating': 4.7, 
                'fee': 2200,
                'qualification': 'MBBS, MS (Obstetrics & Gynecology), PGIMER Chandigarh',
                'clinic': 'Patel Fertility Clinic',
                'address': 'Koramangala, Bangalore',
                'phone': '+91-9876543212',
                'bio': 'Specialist in IVF, IUI, and reproductive endocrinology. Expert in treating infertility issues.'
            },
            {
                'name': 'Divya Joshi', 
                'email': 'dr.divya.joshi@example.com',
                'specialty': 'general_gynecology', 
                'experience': 8, 
                'rating': 4.6, 
                'fee': 1600,
                'qualification': 'MBBS, MD (Gynecology), Grant Medical College Mumbai',
                'clinic': 'Joshi Women\'s Care Center',
                'address': 'Satellite, Ahmedabad',
                'phone': '+91-9876543213',
                'bio': 'Young and enthusiastic gynecologist with focus on adolescent health and preventive care.'
            },
            {
                'name': 'Kavita Singh', 
                'email': 'dr.kavita.singh@example.com',
                'specialty': 'gynecologic_oncology', 
                'experience': 20, 
                'rating': 4.9, 
                'fee': 2500,
                'qualification': 'MBBS, MD (Obstetrics & Gynecology), AIIMS Delhi, Fellowship in Oncology',
                'clinic': 'Singh Cancer Care Center',
                'address': 'T. Nagar, Chennai',
                'phone': '+91-9876543214',
                'bio': 'Leading expert in gynecological cancers and minimally invasive surgery with 20+ years experience.'
            }
        ]
        
        created_count = 0
        for doctor_data in doctors_data:
            name_parts = doctor_data['name'].lower().split()
            username = f"dr.{name_parts[0]}.{name_parts[1]}"
            
            # Delete existing user if exists to recreate fresh
            if User.objects.filter(username=username).exists():
                existing_user = User.objects.get(username=username)
                if hasattr(existing_user, 'doctor_profile'):
                    existing_user.doctor_profile.delete()
                existing_user.delete()
                self.stdout.write(f'🔄 Deleted existing account for {doctor_data["name"]}')
            
            # Create fresh user
            user = User.objects.create_user(
                username=username,
                email=doctor_data['email'],
                password='doctor123',
                first_name=name_parts[0].title(),
                last_name=name_parts[1].title()
            )
            
            # Create doctor profile
            Doctor.objects.create(
                user=user,
                license_number=f"MCI{random.randint(100000, 999999)}",
                specialty=doctor_data['specialty'],
                qualification=doctor_data['qualification'],
                experience_years=doctor_data['experience'],
                consultation_fee=doctor_data['fee'],
                rating=doctor_data['rating'],
                phone_number=doctor_data['phone'],
                clinic_name=doctor_data['clinic'],
                clinic_address=doctor_data['address'],
                bio=doctor_data['bio'],
                status='active',
                is_available_online=True,
                is_accepting_new_patients=True
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'✅ Created: {doctor_data["name"]} ({doctor_data["email"]})'))
        
        # Create sample appointments for some doctors
        self.stdout.write('\n📅 Creating sample appointments...')
        guest_user = User.objects.filter(username='guest').first()
        if guest_user:
            doctors = Doctor.objects.all()
            for i, doctor in enumerate(doctors[:3]):  # Create appointments for first 3 doctors
                for j in range(2):
                    Appointment.objects.create(
                        doctor=doctor,
                        patient=guest_user,
                        patient_name='Test Patient',
                        patient_email='test@example.com',
                        patient_phone='+919999999999',
                        appointment_date=date.today() + timedelta(days=i+j+1),
                        appointment_time='10:00',
                        consultation_fee=doctor.consultation_fee,
                        reason_for_visit='Regular checkup',
                        status='pending' if j == 0 else 'confirmed'
                    )
            self.stdout.write(self.style.SUCCESS('✅ Created sample appointments'))
        
        # Summary
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS(f'🎉 Successfully created {created_count} doctor accounts!'))
        self.stdout.write('\n📋 LOGIN CREDENTIALS:')
        self.stdout.write('=' * 30)
        self.stdout.write('👑 ADMIN ACCOUNT:')
        self.stdout.write('   Email: dr.admin@example.com')
        self.stdout.write('   Password: admin123')
        self.stdout.write('   Role: Super Admin')
        self.stdout.write('')
        self.stdout.write('👩‍⚕️ DOCTOR ACCOUNTS:')
        for doctor_data in doctors_data:
            self.stdout.write(f'   Dr. {doctor_data["name"]}:')
            self.stdout.write(f'     Email: {doctor_data["email"]}')
            self.stdout.write(f'     Password: doctor123')
            self.stdout.write(f'     Specialty: {doctor_data["specialty"].replace("_", " ").title()}')
            self.stdout.write(f'     Rating: ⭐ {doctor_data["rating"]}/5.0')
            self.stdout.write('')
        
        self.stdout.write('🌐 ACCESS DOCTOR DASHBOARD:')
        self.stdout.write('   URL: http://localhost:9000/api/doctors/dashboard-ui/')
        self.stdout.write('   OR: http://localhost:9000/admin/ (for admin)')
        self.stdout.write('\n🚀 Start servers with: ./run_servers.sh')
