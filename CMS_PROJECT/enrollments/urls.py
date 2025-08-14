from django.urls import path
from . import views

urlpatterns = [
    path('enroll/', views.enroll_student, name='enroll_student'),
    path('my/', views.my_enrollments, name='my_enrollments'),
]
