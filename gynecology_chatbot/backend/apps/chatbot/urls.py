from django.urls import path, include
from django.conf import settings

# Conditional URL routing based on USE_FIRESTORE setting
if getattr(settings, 'USE_FIRESTORE', False):
    # Use Firestore views
    from . import firestore_views
    
    urlpatterns = [
        # Conversation endpoints
        path('conversations/', firestore_views.firestore_conversations, name='firestore-conversations'),
        path('conversations/<str:conversation_id>/', firestore_views.firestore_conversation_detail, name='firestore-conversation-detail'),
        path('conversations/<str:conversation_id>/send_message/', firestore_views.firestore_send_message, name='firestore-send-message'),
        
        # Health check
        path('health/', firestore_views.firestore_health, name='firestore-health'),
    ]
else:
    # Use original Django views
    from rest_framework_nested import routers
    from .views import ConversationViewSet, MessageViewSet

    router = routers.SimpleRouter()
    router.register(r'conversations', ConversationViewSet, basename='conversation')

    messages_router = routers.NestedSimpleRouter(router, r'conversations', lookup='conversation')
    messages_router.register(r'messages', MessageViewSet, basename='conversation-messages')

    urlpatterns = [
        path('', include(router.urls)),
        path('', include(messages_router.urls)),
    ]
