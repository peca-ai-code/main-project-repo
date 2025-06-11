import os
import django
import sys
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gynecology_chatbot_project.settings')
django.setup()

from utils.firestore_client import firestore_client

def test_firestore_connection():
    """Test Firestore connection"""
    try:
        # Test creating a simple document
        test_data = {'test': True, 'timestamp': datetime.now()}
        doc_id = firestore_client.create_document('test_collection', test_data)
        print(f"✅ Firestore connection successful. Test document ID: {doc_id}")
        
        # Clean up test document
        firestore_client.delete_document('test_collection', doc_id)
        print("✅ Test document cleaned up")
        return True
    except Exception as e:
        print(f"❌ Firestore connection failed: {e}")
        return False

def backup_sqlite_data():
    """Create a backup of existing SQLite data"""
    import shutil
    backup_path = f"db_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sqlite3"
    try:
        shutil.copy2('db.sqlite3', backup_path)
        print(f"✅ SQLite backup created: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")
        return None

def migrate_users():
    """Migrate users from Django to Firestore"""
    from apps.users.models import User as DjangoUser
    
    users = DjangoUser.objects.all()
    migrated_count = 0
    
    print(f"Migrating {users.count()} users...")
    
    for user in users:
        user_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_of_birth': user.date_of_birth,
            'has_accepted_terms': user.has_accepted_terms,
            'preferred_model': user.preferred_model,
            'show_all_models': user.show_all_models,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'password_hash': user.password
        }
        
        # Use create_document with specific ID
        doc_id = firestore_client.create_document('users', user_data, str(user.id))
        print(f"✅ Created user {user.username} with ID: {doc_id}")
        migrated_count += 1
    
    return migrated_count

def migrate_conversations():
    """Migrate conversations from Django to Firestore"""
    from apps.chatbot.models import Conversation as DjangoConversation
    
    conversations = DjangoConversation.objects.all()
    migrated_count = 0
    
    print(f"Migrating {conversations.count()} conversations...")
    
    for conversation in conversations:
        conversation_data = {
            'user_id': str(conversation.user.id) if conversation.user else '',
            'title': conversation.title,
            'created_at': conversation.created_at,
            'updated_at': conversation.updated_at
        }
        
        # Use create_document with specific ID
        doc_id = firestore_client.create_document('conversations', conversation_data, str(conversation.id))
        print(f"✅ Created conversation '{conversation.title}' with ID: {doc_id}")
        migrated_count += 1
    
    return migrated_count

def migrate_messages():
    """Migrate messages from Django to Firestore"""
    from apps.chatbot.models import Message as DjangoMessage
    
    messages = DjangoMessage.objects.all()
    migrated_count = 0
    
    print(f"Migrating {messages.count()} messages...")
    
    for message in messages:
        message_data = {
            'conversation_id': str(message.conversation.id),
            'content': message.content,
            'message_type': message.message_type,
            'model_name': message.model_name or '',
            'metadata': message.metadata or {},
            'created_at': message.created_at
        }
        
        # Use create_document with specific ID
        doc_id = firestore_client.create_document('messages', message_data, str(message.id))
        print(f"✅ Created message with ID: {doc_id}")
        migrated_count += 1
    
    return migrated_count

def migrate_doctors():
    """Migrate doctors from Django to Firestore"""
    try:
        from doctors.models import Doctor as DjangoDoctor
        
        doctors = DjangoDoctor.objects.all()
        migrated_count = 0
        
        print(f"Migrating {doctors.count()} doctors...")
        
        for doctor in doctors:
            doctor_data = {
                'user_id': str(doctor.user.id),
                'license_number': doctor.license_number,
                'specialty': doctor.specialty,
                'qualification': doctor.qualification,
                'experience_years': doctor.experience_years,
                'clinic_name': doctor.clinic_name,
                'clinic_address': doctor.clinic_address,
                'phone_number': doctor.phone_number,
                'consultation_fee': float(doctor.consultation_fee),
                'rating': float(doctor.rating),
                'total_consultations': doctor.total_consultations,
                'status': doctor.status,
                'is_available_online': doctor.is_available_online,
                'is_accepting_new_patients': doctor.is_accepting_new_patients,
                'bio': doctor.bio,
                'languages_spoken': doctor.languages_spoken,
                'last_active': doctor.last_active
            }
            
            # Use create_document with specific ID
            doc_id = firestore_client.create_document('doctors', doctor_data, str(doctor.id))
            print(f"✅ Created doctor {doctor.user.username} with ID: {doc_id}")
            migrated_count += 1
        
        return migrated_count
    except ImportError:
        print("No doctors app found, skipping doctor migration")
        return 0

def migrate_appointments():
    """Migrate appointments from Django to Firestore"""
    try:
        from doctors.models import Appointment as DjangoAppointment
        
        appointments = DjangoAppointment.objects.all()
        migrated_count = 0
        
        print(f"Migrating {appointments.count()} appointments...")
        
        for appointment in appointments:
            appointment_data = {
                'appointment_id': str(appointment.appointment_id),
                'doctor_id': str(appointment.doctor.id),
                'patient_id': str(appointment.patient.id) if appointment.patient else '',
                'patient_name': appointment.patient_name,
                'patient_email': appointment.patient_email,
                'patient_phone': appointment.patient_phone,
                'patient_age': appointment.patient_age,
                'appointment_date': appointment.appointment_date,
                'appointment_time': appointment.appointment_time,
                'duration_minutes': appointment.duration_minutes,
                'appointment_type': appointment.appointment_type,
                'status': appointment.status,
                'reason_for_visit': appointment.reason_for_visit,
                'doctor_notes': appointment.doctor_notes,
                'patient_notes': appointment.patient_notes,
                'consultation_fee': float(appointment.consultation_fee),
                'payment_status': appointment.payment_status,
                'related_conversation_id': str(appointment.related_conversation.id) if appointment.related_conversation else ''
            }
            
            # Use create_document with specific ID
            doc_id = firestore_client.create_document('appointments', appointment_data, str(appointment.id))
            print(f"✅ Created appointment with ID: {doc_id}")
            migrated_count += 1
        
        return migrated_count
    except ImportError:
        print("No appointments found, skipping appointment migration")
        return 0

def verify_migration():
    """Verify migration by checking Firestore collections"""
    print("\n4. Verifying migration...")
    
    verification_results = {}
    
    # Check each collection
    collections = ['users', 'conversations', 'messages', 'doctors', 'appointments']
    
    for collection in collections:
        try:
            docs = firestore_client.query_collection(collection, limit=5)
            count = len(docs)
            verification_results[collection] = count
            print(f"✅ Found {count} documents in {collection} collection")
            
            if count > 0 and collection == 'users':
                # Show sample user data
                sample_user = docs[0]
                print(f"   Sample user: {sample_user.get('username', 'No username')} ({sample_user.get('email', 'No email')})")
                
        except Exception as e:
            print(f"❌ Error checking {collection}: {e}")
            verification_results[collection] = 0
    
    return verification_results

def main():
    """Main migration function"""
    print("=" * 50)
    print("GYNECOLOGY CHATBOT - FIRESTORE MIGRATION")
    print("=" * 50)
    
    # Step 1: Test Firestore connection
    print("\n1. Testing Firestore connection...")
    if not test_firestore_connection():
        print("❌ Cannot proceed without Firestore connection")
        sys.exit(1)
    
    # Step 2: Backup existing data
    print("\n2. Creating backup of existing data...")
    backup_path = backup_sqlite_data()
    if not backup_path:
        print("⚠️ Warning: Could not create backup, but proceeding...")
    
    # Step 3: Migrate data
    print("\n3. Migrating data to Firestore...")
    
    try:
        # Migrate users
        user_count = migrate_users()
        print(f"✅ Migrated {user_count} users")
        
        # Migrate conversations
        conversation_count = migrate_conversations()
        print(f"✅ Migrated {conversation_count} conversations")
        
        # Migrate messages
        message_count = migrate_messages()
        print(f"✅ Migrated {message_count} messages")
        
        # Migrate doctors (optional)
        doctor_count = migrate_doctors()
        print(f"✅ Migrated {doctor_count} doctors")
        
        # Migrate appointments (optional)
        appointment_count = migrate_appointments()
        print(f"✅ Migrated {appointment_count} appointments")
        
        # Verify migration
        verification_results = verify_migration()
        
        # Migration summary
        total_migrated = user_count + conversation_count + message_count + doctor_count + appointment_count
        print(f"\n📊 Migration Summary:")
        print(f"  Users: {user_count}")
        print(f"  Conversations: {conversation_count}")
        print(f"  Messages: {message_count}")
        print(f"  Doctors: {doctor_count}")
        print(f"  Appointments: {appointment_count}")
        print(f"  Total records migrated: {total_migrated}")
        
        print("\n✅ Migration completed successfully!")
        print("\nNext steps:")
        print("1. Update your .env file to use Firestore: USE_FIRESTORE=True")
        print("2. Restart your Django server")
        print("3. Test the application functionality")
        if backup_path:
            print(f"4. Keep backup file: {backup_path}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
