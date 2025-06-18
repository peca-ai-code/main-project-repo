from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from utils.firestore_client import firestore_client
from utils.llm_utils import generate_ai_responses
from django.conf import settings
import uuid
from datetime import datetime

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # For testing, make it open
def firestore_conversations(request):
    """Handle conversation operations with Firestore"""
    # For testing, use a default user ID if not authenticated
    if request.user.is_authenticated:
        user_id = str(request.user.id)
    else:
        user_id = "2"  # guest user ID
    
    if request.method == 'GET':
        # Get user conversations
        conversations = firestore_client.query_collection(
            'conversations',
            filters=[('user_id', '==', user_id)],
            order_by='updated_at',
            limit=50
        )
        
        conversation_data = []
        for conv in conversations:
            # Get message count for this conversation
            messages = firestore_client.query_collection(
                'messages',
                filters=[('conversation_id', '==', conv['id'])]
            )
            
            conversation_data.append({
                'id': conv['id'],
                'title': conv.get('title', 'New Conversation'),
                'created_at': conv.get('created_at'),
                'updated_at': conv.get('updated_at'),
                'message_count': len(messages)
            })
        
        return Response(conversation_data)
    
    elif request.method == 'POST':
        # Create new conversation
        title = request.data.get('title', 'New Conversation')
        
        conversation_data = {
            'user_id': user_id,
            'title': title
        }
        
        doc_id = firestore_client.create_document('conversations', conversation_data)
        
        return Response({
            'id': doc_id,
            'title': title,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'messages': []
        }, status=status.HTTP_201_CREATED)

@api_view(['GET', 'DELETE'])
@permission_classes([AllowAny])
def firestore_conversation_detail(request, conversation_id):
    """Handle individual conversation operations"""
    if request.user.is_authenticated:
        user_id = str(request.user.id)
    else:
        user_id = "2"  # guest user
    
    # Get conversation
    conversation = firestore_client.get_document('conversations', conversation_id)
    if not conversation or conversation.get('user_id') != user_id:
        return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        # Get conversation with messages
        messages = firestore_client.query_collection(
            'messages',
            filters=[('conversation_id', '==', conversation_id)],
            order_by='created_at'
        )
        
        message_data = []
        for msg in messages:
            message_data.append({
                'id': msg['id'],
                'content': msg.get('content', ''),
                'message_type': msg.get('message_type', 'user'),
                'model_name': msg.get('model_name', ''),
                'metadata': msg.get('metadata', {}),
                'created_at': msg.get('created_at')
            })
        
        return Response({
            'id': conversation['id'],
            'title': conversation.get('title', 'New Conversation'),
            'created_at': conversation.get('created_at'),
            'updated_at': conversation.get('updated_at'),
            'messages': message_data
        })
    
    elif request.method == 'DELETE':
        # Clear conversation messages
        messages = firestore_client.query_collection(
            'messages',
            filters=[('conversation_id', '==', conversation_id)]
        )
        
        for message in messages:
            firestore_client.delete_document('messages', message['id'])
        
        return Response({'message': 'Conversation cleared successfully'})

@api_view(['POST'])
@permission_classes([AllowAny])
def firestore_send_message(request, conversation_id):
    """Send message and get AI response using Firestore"""
    if request.user.is_authenticated:
        user_id = str(request.user.id)
    else:
        user_id = "2"  # guest user
    
    # Verify conversation exists
    conversation = firestore_client.get_document('conversations', conversation_id)
    if not conversation or conversation.get('user_id') != user_id:
        return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
    
    user_message = request.data.get('message', '').strip()
    if not user_message:
        return Response({'error': 'Message content is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Save user message
        user_msg_data = {
            'conversation_id': conversation_id,
            'content': user_message,
            'message_type': 'user'
        }
        user_msg_id = firestore_client.create_document('messages', user_msg_data)
        
        # Get conversation history for AI context (simplified for now)
        messages = firestore_client.query_collection(
            'messages',
            filters=[('conversation_id', '==', conversation_id)],
            order_by='created_at'
        )
        
        # Convert messages to expected format for LLM
        message_history = []
        for msg in messages:
            class MockMessage:
                def __init__(self, content, message_type, model_name=None):
                    self.content = content
                    self.message_type = message_type
                    self.model_name = model_name
            
            message_history.append(MockMessage(
                msg.get('content', ''),
                msg.get('message_type', 'user'),
                msg.get('model_name', '')
            ))
        
        # Generate AI responses
        response_data = generate_ai_responses(user_message, message_history)
        
        best_model = response_data["best_model"]
        best_response = response_data["best_response"]
        explanation = response_data["explanation"]
        
        # Save AI response
        ai_msg_data = {
            'conversation_id': conversation_id,
            'content': best_response,
            'message_type': 'assistant',
            'model_name': best_model,
            'metadata': {
                "explanation": explanation,
                "evaluated": True,
                "all_responses": response_data.get("all_responses", {})
            }
        }
        ai_msg_id = firestore_client.create_document('messages', ai_msg_data)
        
        # Update conversation timestamp
        firestore_client.update_document('conversations', conversation_id, {
            'updated_at': datetime.now()
        })
        
        return Response({
            "message_id": ai_msg_id,
            "content": best_response,
            "model_name": best_model,
            "explanation": explanation
        })
        
    except Exception as e:
        return Response({
            'error': f'Error generating AI response: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Health check for Firestore
@api_view(['GET'])
@permission_classes([AllowAny])
def firestore_health(request):
    """Health check for Firestore connection"""
    try:
        # Test Firestore connection
        test_data = {'health_check': True, 'timestamp': datetime.now()}
        doc_id = firestore_client.create_document('health_check', test_data)
        firestore_client.delete_document('health_check', doc_id)
        
        return Response({
            'status': 'ok',
            'message': 'Firestore connection healthy',
            'use_firestore': getattr(settings, 'USE_FIRESTORE', False)
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Firestore connection failed: {str(e)}',
            'use_firestore': getattr(settings, 'USE_FIRESTORE', False)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
