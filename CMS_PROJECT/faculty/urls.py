from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, FacultyViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'faculty', FacultyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
