from django.urls import path
from . import views

urlpatterns = [
    path('programs/', views.list_programs, name='list_programs'),
    path('programs/add/', views.add_program, name='add_program'),
    path('courses/', views.list_courses, name='list_courses'),
    path('courses/add/', views.add_course, name='add_course'),
]
