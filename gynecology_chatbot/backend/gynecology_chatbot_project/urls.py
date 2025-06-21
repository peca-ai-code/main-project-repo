from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from utils.views import health_check, redirect_to_admin

urlpatterns = [
    # Redirect root to admin
    path('', redirect_to_admin),
    
    # Admin site
    path('admin/', admin.site.urls),
    
    # Health check endpoint
    path('api/', include('utils.urls')),
    
    # API endpoints
    path('api/users/', include('apps.users.urls')),
    path('api/chatbot/', include('apps.chatbot.urls')),
    path('api/doctors/', include('doctors.urls')),
    path('api/appointments/', include('apps.appointments_api.urls')),  # New appointment API

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Appointments web app
    path('appointments/', include('appointments.urls')),

    path('api/oauth/', include('oauth_integration.urls')),
    path('accounts/', include('allauth.urls')),
]

# Add debug information
if settings.DEBUG:
    from django.http import JsonResponse
    
    def debug_info(request):
        return JsonResponse({
            'use_firestore': getattr(settings, 'USE_FIRESTORE', False),
            'google_cloud_project': getattr(settings, 'GOOGLE_CLOUD_PROJECT', 'Not configured'),
            'database_engine': settings.DATABASES['default']['ENGINE']
        })
    
    urlpatterns += [
        path('api/debug/', debug_info, name='debug_info'),
    ]
# Add doctor dashboard direct access
if 'doctors-dashboard' not in [pattern.name for pattern in urlpatterns if hasattr(pattern, 'name')]:
    urlpatterns += [
        path('doctors-dashboard/', include('doctors.urls')),
    ]