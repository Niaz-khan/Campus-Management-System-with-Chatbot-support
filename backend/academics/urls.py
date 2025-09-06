from django.urls import path
from .views import (
    BatchListCreateView, BatchDetailView,
    ProgramListCreateView, ProgramDetailView
)

urlpatterns = [
    path('batches/', BatchListCreateView.as_view(), name='batch-list-create'),
    path('batches/<int:pk>/', BatchDetailView.as_view(), name='batch-detail'),
    path('programs/', ProgramListCreateView.as_view(), name='program-list-create'),
    path('programs/<int:pk>/', ProgramDetailView.as_view(), name='program-detail'),
]
