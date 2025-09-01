from django.urls import path
from .views import StudentListView, StudentDetailView, MyStudentProfileView

urlpatterns = [
    path('', StudentListView.as_view(), name='student-list'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('me/', MyStudentProfileView.as_view(), name='my-student-profile'),
]
