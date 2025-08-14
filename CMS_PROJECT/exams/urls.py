from django.urls import path
from . import views

urlpatterns = [
    path('exams/', views.list_exams, name='list_exams'),
    path('exams/add/', views.create_exam, name='create_exam'),
    path('results/', views.list_exam_results, name='list_exam_results'),
    path('results/add/', views.add_exam_result, name='add_exam_result'),
    path('transcript/', views.my_transcript, name='my_transcript'),
]
