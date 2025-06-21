import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gynecology_chatbot_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from doctors.models import Doctor

User = get_user_model()

# Create or get admin user
admin_user, created = User.objects.get_or_create(
    email='dr.admin@example.com',
    defaults={
        'username': 'dr.admin',
        'first_name': 'Admin',
        'last_name': 'Doctor',
        'is_staff': True,
        'is_superuser': True,
        'is_active': True
    }
)

# Set password
admin_user.set_password('admin123')
admin_user.save()

print(f'Admin user: {admin_user.email} ({"created" if created else "updated"})')

# Create or get doctor profile
doctor, doctor_created = Doctor.objects.get_or_create(
    user=admin_user,
    defaults={
        'license_number': 'MCI999999',
        'specialty': 'general_gynecology',
        'qualification': 'MBBS, MD (Obstetrics & Gynecology), AIIMS',
        'experience_years': 20,
        'consultation_fee': 2500.00,
        'rating': 5.0,
        'phone_number': '+919999999999',
        'clinic_name': 'Admin Medical Center',
        'clinic_address': 'Medical Complex, Delhi',
        'bio': 'Administrative doctor account.',
        'status': 'active',
        'is_available_online': True,
        'is_accepting_new_patients': True
    }
)

print(f'Doctor profile: {doctor.full_name} ({"created" if doctor_created else "updated"})')
print(f'Login credentials: dr.admin@example.com / admin123')
