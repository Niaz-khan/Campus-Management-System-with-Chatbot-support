from django.urls import path
from .views import FacultyListCreateView, FacultyDetailView, MyFacultyProfileView

urlpatterns = [
    path('', FacultyListCreateView.as_view(), name='faculty-list-create'),
    path('<int:pk>/', FacultyDetailView.as_view(), name='faculty-detail'),
    path('me/', MyFacultyProfileView.as_view(), name='my-faculty-profile'),
]
