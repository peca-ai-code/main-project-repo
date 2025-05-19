from rest_framework import serializers
from .models import Doctor, Specialty, Referral

class SpecialtySerializer(serializers.ModelSerializer):
    """Serializer for medical specialties."""
    
    class Meta:
        model = Specialty
        fields = ('id', 'name', 'description')

class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for doctor profiles."""
    specialty_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = ('id', 'first_name', 'last_name', 'specialty', 'specialty_name',
                  'credentials', 'bio', 'photo', 'email', 'phone', 'website',
                  'address', 'city', 'state', 'zip_code', 'country',
                  'is_available', 'slug')
    
    def get_specialty_name(self, obj):
        return obj.specialty.name if obj.specialty else None

class DoctorListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing doctors."""
    specialty_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = ('id', 'first_name', 'last_name', 'credentials', 
                  'specialty', 'specialty_name', 'city', 'state', 'slug')
    
    def get_specialty_name(self, obj):
        return obj.specialty.name if obj.specialty else None

class ReferralSerializer(serializers.ModelSerializer):
    """Serializer for doctor referrals."""
    doctor_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Referral
        fields = ('id', 'doctor', 'doctor_name', 'reason', 'created_at')
        read_only_fields = ('id', 'created_at')
    
    def get_doctor_name(self, obj):
        return str(obj.doctor)
    
    def create(self, validated_data):
        # Associate with current user
        user = self.context['request'].user
        validated_data['user'] = user
        
        # Optionally associate with current conversation
        conversation_id = self.context['request'].data.get('conversation_id')
        if conversation_id:
            from apps.chatbot.models import Conversation
            try:
                conversation = Conversation.objects.get(id=conversation_id, user=user)
                validated_data['conversation'] = conversation
            except Conversation.DoesNotExist:
                pass
        
        return super().create(validated_data)
