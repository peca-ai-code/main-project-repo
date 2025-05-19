from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from utils.views import health_check, redirect_to_admin

urlpatterns = [
    # Redirect root to admin
    path('', redirect_to_admin),
    
    # Admin site
    path('admin/', admin.site.urls),
    
    # Health check endpoint
    path('api/health/', health_check),
    
    # API endpoints
    path('api/users/', include('apps.users.urls')),
    path('api/chatbot/', include('apps.chatbot.urls')),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
