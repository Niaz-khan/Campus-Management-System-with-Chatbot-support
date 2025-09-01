from django.urls import path
from .views import EnrollmentListCreateView, EnrollmentDetailView, MyEnrollmentsView

urlpatterns = [
    path('', EnrollmentListCreateView.as_view(), name='enrollment-list-create'),
    path('<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path('my/', MyEnrollmentsView.as_view(), name='my-enrollments'),
]
