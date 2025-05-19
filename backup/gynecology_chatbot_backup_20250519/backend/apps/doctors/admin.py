from django.contrib import admin
from .models import Doctor, Specialty, Referral

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'specialty', 'credentials', 'city', 'is_available')
    list_filter = ('specialty', 'is_available', 'city', 'state')
    search_fields = ('first_name', 'last_name', 'bio')
    prepopulated_fields = {'slug': ('first_name', 'last_name')}

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('doctor__first_name', 'doctor__last_name', 'user__email', 'reason')
