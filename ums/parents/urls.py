from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.ParentProfileView.as_view(), name='parent-me'),
    path('my-students/', views.ParentLinkedStudentsView.as_view(), name='parent-my-students'),
    path('dashboard/<int:student_id>/', views.ParentStudentDashboardView.as_view(), name='parent-student-dashboard'),
]
