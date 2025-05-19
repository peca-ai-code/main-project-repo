from rest_framework import serializers
from .models import Conversation, Message, AIModelResponse

class AIModelResponseSerializer(serializers.ModelSerializer):
    """Serializer for AI model responses."""
    
    class Meta:
        model = AIModelResponse
        fields = ('id', 'model_name', 'content', 'created_at')

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for chat messages."""
    model_responses = AIModelResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Message
        fields = ('id', 'content', 'message_type', 'created_at', 'model_name', 'model_responses')

class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for chat conversations."""
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ('id', 'title', 'created_at', 'updated_at', 'messages')

class ConversationListSerializer(serializers.ModelSerializer):
    """Serializer for listing conversations (without messages)."""
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ('id', 'title', 'created_at', 'updated_at', 'message_count')
    
    def get_message_count(self, obj):
        return obj.messages.count()

class ChatInputSerializer(serializers.Serializer):
    """Serializer for chat input from users."""
    message = serializers.CharField(required=True)
    conversation_id = serializers.IntegerField(required=False)
    show_all_models = serializers.BooleanField(required=False, default=True)
    primary_model = serializers.CharField(required=False, default='openai')
