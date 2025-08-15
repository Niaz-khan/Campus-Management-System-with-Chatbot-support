from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FeeStructureViewSet, FeeChallanViewSet, 
    PaymentViewSet, ScholarshipViewSet, FeeSummaryViewSet
)

router = DefaultRouter()
router.register(r'fee-structures', FeeStructureViewSet)
router.register(r'challans', FeeChallanViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'scholarships', ScholarshipViewSet)
router.register(r'summary', FeeSummaryViewSet, basename='fee-summary')

urlpatterns = [
    path('', include(router.urls)),
]
