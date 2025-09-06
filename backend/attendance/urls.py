from django.urls import path
from .views import (
    FacultyAttendanceCreateView,
    AttendanceFacultyListView,
    FacultyAttendanceUpdateView
)
from .views import StudentAttendanceListView

urlpatterns = [
    # Faculty APIs
    path('faculty/mark/', FacultyAttendanceCreateView.as_view(), name='faculty-attendance-mark'),
    path('faculty/list/', AttendanceFacultyListView.as_view(), name='faculty-attendance-list'),
    path('faculty/update/<int:pk>/', FacultyAttendanceUpdateView.as_view(), name='faculty-attendance-update'),

    # Student APIs
    path('student/list/', StudentAttendanceListView.as_view(), name='student-attendance-list'),
]
