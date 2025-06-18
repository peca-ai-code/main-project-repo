from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    DoctorProfileViewSet, DoctorDashboardViewSet, AppointmentManagementViewSet,
    PatientQueryManagementViewSet, doctor_dashboard_view, CustomTokenObtainPairView,
    DoctorRegistrationView
)

router = DefaultRouter()
router.register(r'profile', DoctorProfileViewSet, basename='doctor-profile')
router.register(r'dashboard', DoctorDashboardViewSet, basename='doctor-dashboard')
router.register(r'appointments', AppointmentManagementViewSet, basename='doctor-appointments')
router.register(r'queries', PatientQueryManagementViewSet, basename='doctor-queries')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard-ui/', doctor_dashboard_view, name='doctor-dashboard-ui'),
    path('token/', CustomTokenObtainPairView.as_view(), name='doctor-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='doctor-token-refresh'),
    path('register/', DoctorRegistrationView.as_view(), name='doctor-register'),
]
