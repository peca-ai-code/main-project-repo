from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Conversation, Message, AIModelResponse
from .serializers import (
    ConversationSerializer, ConversationListSerializer,
    MessageSerializer, ChatInputSerializer
)
from utils.llm_utils import generate_ai_responses

class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for chat conversations."""
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return conversations for the current user."""
        return Conversation.objects.filter(user=self.request.user).order_by('-updated_at')
    
    def get_serializer_class(self):
        """Use different serializers for list and detail views."""
        if self.action == 'list':
            return ConversationListSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        """Associate the conversation with the current user."""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send a message in a conversation and get AI responses."""
        conversation = self.get_object()
        serializer = ChatInputSerializer(data=request.data)
        
        if serializer.is_valid():
            user_message = serializer.validated_data['message']
            show_all_models = serializer.validated_data.get('show_all_models', True)
            primary_model = serializer.validated_data.get('primary_model', 'openai')
            
            # Save user message
            message = Message.objects.create(
                conversation=conversation,
                content=user_message,
                message_type='user'
            )
            
            # Get conversation history
            history = Message.objects.filter(conversation=conversation).order_by('created_at')
            
            # Generate AI responses
            try:
                responses = generate_ai_responses(user_message, history, primary_model)
                
                # Save primary response as assistant message
                assistant_message = Message.objects.create(
                    conversation=conversation,
                    content=responses[primary_model],
                    message_type='assistant',
                    model_name=primary_model
                )
                
                # Save all model responses for comparison
                for model_name, response_text in responses.items():
                    AIModelResponse.objects.create(
                        message=assistant_message,
                        model_name=model_name,
                        content=response_text
                    )
                
                # Return the updated conversation
                return Response(self.get_serializer(conversation).data)
            
            except Exception as e:
                return Response(
                    {'error': f'Error generating AI responses: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'])
    def clear(self, request, pk=None):
        """Clear all messages in a conversation."""
        conversation = self.get_object()
        conversation.messages.all().delete()
        return Response({"message": "Conversation cleared successfully"})

class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for messages (read-only)."""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return messages for a specific conversation."""
        conversation_id = self.kwargs.get('conversation_pk')
        return Message.objects.filter(
            conversation_id=conversation_id,
            conversation__user=self.request.user
        ).order_by('created_at')
