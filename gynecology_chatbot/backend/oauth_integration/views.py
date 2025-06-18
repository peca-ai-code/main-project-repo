from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import datetime
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
def oauth_sync(request):
    """Sync OAuth user data with both Django and Firestore"""
    try:
        data = request.data
        email = data.get('email')
        name = data.get('name', '')
        given_name = data.get('given_name', '')
        family_name = data.get('family_name', '')
        picture = data.get('picture', '')
        provider = data.get('provider', 'google')
        provider_id = data.get('provider_id', '')
        access_token = data.get('access_token', '')
        
        if not email:
            return Response({'error': 'Email is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        print(f"🔄 Syncing OAuth user: {email}")
        
        # ALWAYS create/update Django user for JWT authentication
        django_user, user_created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'first_name': given_name,
                'last_name': family_name,
                'has_accepted_terms': True,
            }
        )
        
        # Update existing Django user
        if not user_created:
            django_user.first_name = given_name
            django_user.last_name = family_name
            django_user.has_accepted_terms = True
            django_user.save()
        
        print(f"✅ Django user {'created' if user_created else 'updated'}: {django_user.id}")
        
        # Create or update OAuth profile in Django
        oauth_profile, oauth_created = OAuthProfile.objects.get_or_create(
            user=django_user,
            provider=provider,
            defaults={
                'provider_id': provider_id,
                'access_token': access_token,
                'profile_picture_url': picture,
                'is_connected': True,
            }
        )
        
        if not oauth_created:
            oauth_profile.access_token = access_token
            oauth_profile.profile_picture_url = picture
            oauth_profile.is_connected = True
            oauth_profile.save()
        
        print(f"✅ OAuth profile {'created' if oauth_created else 'updated'}")
        
        # ALSO store in Firestore if enabled
        if getattr(settings, 'USE_FIRESTORE', False):
            from utils.firestore_client import firestore_client
            
            # Store user in Firestore with Django user ID as reference
            firestore_user_data = {
                'django_user_id': django_user.id,  # Reference to Django user
                'username': email,
                'email': email,
                'first_name': given_name,
                'last_name': family_name,
                'has_accepted_terms': True,
                'preferred_model': 'gemini',
                'show_all_models': True,
                'is_active': True,
                'is_staff': False,
                'date_joined': datetime.now(),
                'last_login': datetime.now(),
            }
            
            # Check if user exists in Firestore
            existing_firestore_users = firestore_client.query_collection(
                'users', 
                filters=[('email', '==', email)]
            )
            
            if existing_firestore_users:
                # Update existing Firestore user
                firestore_user_id = existing_firestore_users[0]['id']
                firestore_client.update_document('users', firestore_user_id, firestore_user_data)
                print(f"✅ Updated Firestore user: {firestore_user_id}")
            else:
                # Create new Firestore user
                firestore_user_id = firestore_client.create_document('users', firestore_user_data)
                print(f"✅ Created Firestore user: {firestore_user_id}")
            
            # Store OAuth profile in Firestore
            firestore_oauth_data = {
                'django_user_id': django_user.id,
                'firestore_user_id': firestore_user_id,
                'provider': provider,
                'provider_id': provider_id,
                'access_token': access_token,
                'profile_picture_url': picture,
                'is_connected': True,
                'updated_at': datetime.now(),
            }
            
            # Check if OAuth profile exists in Firestore
            existing_oauth = firestore_client.query_collection(
                'oauth_profiles',
                filters=[('django_user_id', '==', django_user.id), ('provider', '==', provider)]
            )
            
            if existing_oauth:
                firestore_client.update_document('oauth_profiles', existing_oauth[0]['id'], firestore_oauth_data)
                print(f"✅ Updated Firestore OAuth profile")
            else:
                firestore_oauth_data['created_at'] = datetime.now()
                firestore_client.create_document('oauth_profiles', firestore_oauth_data)
                print(f"✅ Created Firestore OAuth profile")
        
        # Generate JWT tokens using Django user (integer ID)
        refresh = RefreshToken.for_user(django_user)
        
        print(f"✅ Generated JWT tokens for Django user ID: {django_user.id}")
        
        return Response({
            'success': True,
            'user': {
                'id': django_user.id,  # Django integer ID for JWT
                'email': email,
                'first_name': given_name,
                'last_name': family_name,
                'profile_picture': picture,
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            'created': user_created,
        })
        
    except Exception as e:
        print(f"❌ OAuth sync error: {str(e)}")
        import traceback
        traceback.print_exc()
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