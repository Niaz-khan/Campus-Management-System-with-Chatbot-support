from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExamViewSet, ExamScheduleViewSet, ExamResultViewSet,
    GradeViewSet, TranscriptViewSet, ExamAttendanceViewSet, ExamAnalyticsViewSet
)

router = DefaultRouter()
router.register(r'exams', ExamViewSet)
router.register(r'schedules', ExamScheduleViewSet)
router.register(r'results', ExamResultViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'transcripts', TranscriptViewSet)
router.register(r'attendance', ExamAttendanceViewSet)
router.register(r'analytics', ExamAnalyticsViewSet, basename='exam-analytics')

urlpatterns = [
    path('', include(router.urls)),
]
