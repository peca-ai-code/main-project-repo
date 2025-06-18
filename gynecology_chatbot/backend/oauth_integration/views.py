from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token
import requests as http_requests
from .models import OAuthProfile
import json

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def google_oauth_login(request):
    """Handle Google OAuth login from Chainlit"""
    try:
        auth_code = request.data.get('code')
        if not auth_code:
            return Response({'error': 'Authorization code is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Exchange authorization code for tokens
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
            'code': auth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.OAUTH_REDIRECT_URI,
        }
        
        token_response = http_requests.post(token_url, data=token_data)
        token_json = token_response.json()
        
        if 'access_token' not in token_json:
            return Response({'error': 'Failed to obtain access token'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Get user info from Google
        user_info_response = http_requests.get(
            f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={token_json['access_token']}"
        )
        user_info = user_info_response.json()
        
        # Create or get user
        user, created = User.objects.get_or_create(
            email=user_info['email'],
            defaults={
                'username': user_info['email'],
                'first_name': user_info.get('given_name', ''),
                'last_name': user_info.get('family_name', ''),
                'has_accepted_terms': True,
            }
        )
        
        # Create or update OAuth profile
        oauth_profile, _ = OAuthProfile.objects.get_or_create(
            user=user,
            provider='google',
            defaults={
                'provider_id': user_info['id'],
                'access_token': token_json['access_token'],
                'refresh_token': token_json.get('refresh_token', ''),
                'profile_picture_url': user_info.get('picture', ''),
                'is_connected': True,
            }
        )
        
        # Update existing profile
        oauth_profile.access_token = token_json['access_token']
        oauth_profile.profile_picture_url = user_info.get('picture', '')
        oauth_profile.is_connected = True
        oauth_profile.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile_picture': oauth_profile.profile_picture_url,
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            'created': created,
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def disconnect_oauth(request):
    """Disconnect OAuth account"""
    try:
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        
        oauth_profile = OAuthProfile.objects.get(user=user, provider='google')
        oauth_profile.is_connected = False
        oauth_profile.access_token = ''
        oauth_profile.refresh_token = ''
        oauth_profile.save()
        
        return Response({'success': True, 'message': 'OAuth account disconnected'})
        
    except (User.DoesNotExist, OAuthProfile.DoesNotExist):
        return Response({'error': 'OAuth profile not found'}, 
                      status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def oauth_config(request):
    """Get OAuth configuration for frontend"""
    return Response({
        'google_client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'redirect_uri': settings.OAUTH_REDIRECT_URI,
        'scope': 'openid email profile',
    })