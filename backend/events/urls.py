from django.urls import path
from . import views

urlpatterns = [
    # Faculty/Admin
    path('faculty/events/', views.EventListCreateView.as_view(), name='event-list-create'),
    path('faculty/events/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('faculty/issue-certificate/', views.IssueCertificateView.as_view(), name='issue-certificate'),

    # Student
    path('student/available/', views.AvailableEventsView.as_view(), name='available-events'),
    path('student/register/', views.RegisterEventView.as_view(), name='register-event'),
    path('student/my-registrations/', views.MyEventRegistrationsView.as_view(), name='my-event-registrations'),
]
