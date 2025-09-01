from django.urls import path
from .views import ExamListCreateView, ExamDetailView

urlpatterns = [
    path('', ExamListCreateView.as_view(), name='exam-list-create'),
    path('<int:pk>/', ExamDetailView.as_view(), name='exam-detail'),
]
