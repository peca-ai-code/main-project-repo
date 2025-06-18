from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model, authenticate
from .models import Doctor, Appointment, PatientQuery

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField()
        self.fields['username'] = serializers.CharField(required=False)
        del self.fields['username']  # Remove username field
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'),
                              username=email, password=password)
            
            if not user:
                # Try to find user by email and authenticate
                try:
                    user_obj = User.objects.get(email=email)
                    user = authenticate(request=self.context.get('request'),
                                      username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user and user.is_active:
                refresh = self.get_token(user)
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            else:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Email and password required')

class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['id', 'full_name', 'user_email', 'specialty', 'experience_years', 'rating', 'consultation_fee', 'status', 'bio', 'phone_number']

class AppointmentSerializer(serializers.ModelSerializer):
    patient_display_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Appointment
        fields = ['appointment_id', 'patient_display_name', 'appointment_date', 'appointment_time', 'status', 'appointment_type', 'reason_for_visit']

class QuerySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    
    class Meta:
        model = PatientQuery
        fields = ['id', 'patient_name', 'query_text', 'ai_response', 'severity_score', 'doctor_reviewed']

class DoctorRegistrationSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)
    qualification = serializers.CharField(max_length=500)
    experience_years = serializers.IntegerField(min_value=0)
    specialty = serializers.CharField(max_length=100)
    clinic_name = serializers.CharField(max_length=200, required=False)
    message = serializers.CharField(max_length=1000, required=False)
