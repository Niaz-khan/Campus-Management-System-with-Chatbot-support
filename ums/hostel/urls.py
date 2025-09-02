from django.urls import path
from . import views 

urlpatterns = [
    # Faculty/Admin
    path('faculty/hostels/', views.HostelListCreateView.as_view(), name='hostel-list-create'),
    path('faculty/hostels/<int:pk>/', views.HostelDetailView.as_view(), name='hostel-detail'),

    path('faculty/rooms/', views.RoomListCreateView.as_view(), name='room-list-create'),
    path('faculty/rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room-detail'),

    path('faculty/allocate/', views.RoomAllocateView.as_view(), name='room-allocate'),
    path('faculty/allocations/<int:pk>/vacate/', views.RoomVacateView.as_view(), name='room-vacate'),

    path('faculty/violations/', views.ViolationListView.as_view(), name='violation-list'),
    path('faculty/violations/create/', views.ViolationCreateView.as_view(), name='violation-create'),
    path('faculty/violations/<int:pk>/', views.ViolationDetailView.as_view(), name='violation-detail'),

    # Student
    path('student/my-allocation/', views.StudentMyAllocationView.as_view(), name='student-my-allocation'),
    path('student/available-rooms/', views.StudentAvailableRoomsView.as_view(), name='student-available-rooms'),
    path('student/violations/', views.StudentViolationsView.as_view(), name='student-violations'),
]
