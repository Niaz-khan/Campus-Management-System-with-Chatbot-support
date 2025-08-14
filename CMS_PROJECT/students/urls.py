from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.my_profile, name='my_profile'),
    path('admin/students/', views.list_students, name='list_students'),
    path('admin/students/add/', views.add_student, name='add_student'),
    path('transcript/', views.student_transcript_view, name='student_transcript'),
]