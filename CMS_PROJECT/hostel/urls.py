from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HostelViewSet, RoomViewSet, StudentViewSet, StaffViewSet,
    MaintenanceViewSet, VisitorViewSet, ComplaintViewSet,
    PaymentViewSet, NoticeViewSet, HostelAnalyticsViewSet
)

router = DefaultRouter()
router.register(r'hostels', HostelViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'students', StudentViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'maintenance', MaintenanceViewSet)
router.register(r'visitors', VisitorViewSet)
router.register(r'complaints', ComplaintViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'notices', NoticeViewSet)
router.register(r'analytics', HostelAnalyticsViewSet, basename='hostel-analytics')

urlpatterns = [
    path('', include(router.urls)),
]
