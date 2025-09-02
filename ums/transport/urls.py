from django.urls import path
from . import views

urlpatterns = [
    # Faculty/Admin
    path('faculty/routes/', views.RouteListCreateView.as_view(), name='route-list-create'),
    path('faculty/routes/<int:pk>/', views.RouteDetailView.as_view(), name='route-detail'),
    path('faculty/vehicles/', views.VehicleListCreateView.as_view(), name='vehicle-list-create'),
    path('faculty/vehicles/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle-detail'),
    path('faculty/pass/issue/', views.IssueTransportPassView.as_view(), name='issue-pass'),
    path('faculty/pass/<int:pk>/revoke/', views.RevokeTransportPassView.as_view(), name='revoke-pass'),

    # Student
    path('student/my-pass/', views.StudentMyTransportPassView.as_view(), name='student-my-pass'),
    path('student/available-routes/', views.StudentAvailableRoutesView.as_view(), name='student-available-routes'),
]
