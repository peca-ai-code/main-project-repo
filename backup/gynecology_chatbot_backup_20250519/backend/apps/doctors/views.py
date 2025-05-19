from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Doctor, Specialty, Referral
from .serializers import (
    DoctorSerializer, DoctorListSerializer, 
    SpecialtySerializer, ReferralSerializer
)

class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for doctor profiles (read-only)."""
    queryset = Doctor.objects.filter(is_available=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['specialty', 'city', 'state']
    search_fields = ['first_name', 'last_name', 'specialty__name', 'city']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DoctorListSerializer
        return DoctorSerializer
    
    def get_permissions(self):
        """Allow anyone to see doctor listings."""
        return [permissions.AllowAny()]

class SpecialtyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for medical specialties (read-only)."""
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [permissions.AllowAny]

class ReferralViewSet(viewsets.ModelViewSet):
    """ViewSet for doctor referrals."""
    serializer_class = ReferralSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return referrals for the current user."""
        return Referral.objects.filter(user=self.request.user).order_by('-created_at')
