from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, SpecialtyViewSet, ReferralViewSet

router = DefaultRouter()
router.register(r'profiles', DoctorViewSet)
router.register(r'specialties', SpecialtyViewSet)
router.register(r'referrals', ReferralViewSet, basename='referral')

urlpatterns = [
    path('', include(router.urls)),
]
