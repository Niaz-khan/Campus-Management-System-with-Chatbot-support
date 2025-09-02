from django.urls import path
from .views import (
    ExamListCreateView, ExamDetailView,
    GradeListCreateView, GradeDetailView, MyGradesView,
    MyGPAView, PublishExamResultsView, LockExamResultsView
)

urlpatterns = [
    path('', ExamListCreateView.as_view(), name='exam-list-create'),
    path('<int:pk>/', ExamDetailView.as_view(), name='exam-detail'),

    path('grades/', GradeListCreateView.as_view(), name='grade-list-create'),
    path('grades/<int:pk>/', GradeDetailView.as_view(), name='grade-detail'),
    path('grades/my/', MyGradesView.as_view(), name='my-grades'),
    path('grades/my/gpa/', MyGPAView.as_view(), name='my-gpa'),
    path('<int:exam_id>/publish/', PublishExamResultsView.as_view(), name='publish-exam-results'),
    path('<int:exam_id>/lock/', LockExamResultsView.as_view(), name='lock-exam-results'),
]
