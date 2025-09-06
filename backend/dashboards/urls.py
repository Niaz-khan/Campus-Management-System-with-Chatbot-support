from django.urls import path
from .views import (
    AdminDashboardView, DepartmentDashboardView,
    FacultyDashboardView, StudentDashboardView
)

urlpatterns = [
    path('admin/', AdminDashboardView.as_view(), name='dashboard-admin'),
    path('department/', DepartmentDashboardView.as_view(), name='dashboard-department'),  # HOD/Coordinator
    path('faculty/', FacultyDashboardView.as_view(), name='dashboard-faculty'),
    path('student/', StudentDashboardView.as_view(), name='dashboard-student'),
]
