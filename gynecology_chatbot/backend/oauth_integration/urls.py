from django.urls import path
from . import views

urlpatterns = [
    path('google/login/', views.google_oauth_login, name='google-oauth-login'),
    path('disconnect/', views.disconnect_oauth, name='disconnect-oauth'),
    path('config/', views.oauth_config, name='oauth-config'),
]
