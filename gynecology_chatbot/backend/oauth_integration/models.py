from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class OAuthProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='oauth_profile')
    provider = models.CharField(max_length=20, default='google')
    provider_id = models.CharField(max_length=100)
    access_token = models.TextField(blank=True)
    refresh_token = models.TextField(blank=True)
    token_expires_at = models.DateTimeField(null=True, blank=True)
    profile_picture_url = models.URLField(blank=True)
    is_connected = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['provider', 'provider_id']
    
    def __str__(self):
        return f"{self.user.email} - {self.provider}"