from django.db import models
from django.utils.text import slugify

class Specialty(models.Model):
    """Medical specialties for doctors."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Specialties"
    
    def __str__(self):
        return self.name

class Doctor(models.Model):
    """Model for doctor profiles."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.ForeignKey(
        Specialty, 
        on_delete=models.SET_NULL,
        related_name='doctors',
        null=True
    )
    credentials = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='doctor_photos/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    is_available = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        credentials = f", {self.credentials}" if self.credentials else ""
        return f"Dr. {self.first_name} {self.last_name}{credentials}"

class Referral(models.Model):
    """Model for storing doctor referrals from the chatbot."""
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='referrals',
        null=True,
        blank=True
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='referrals'
    )
    conversation = models.ForeignKey(
        'chatbot.Conversation',
        on_delete=models.SET_NULL,
        related_name='referrals',
        null=True,
        blank=True
    )
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Referral to {self.doctor} - {self.created_at.strftime('%Y-%m-%d')}"
