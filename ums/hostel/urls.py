from django.urls import path
from .views import faculty as faculty_views
from .views import student as student_views

urlpatterns = [
    # Faculty/Admin
    path('faculty/hostels/', faculty_views.HostelListCreateView.as_view(), name='hostel-list-create'),
    path('faculty/hostels/<int:pk>/', faculty_views.HostelDetailView.as_view(), name='hostel-detail'),

    path('faculty/rooms/', faculty_views.RoomListCreateView.as_view(), name='room-list-create'),
    path('faculty/rooms/<int:pk>/', faculty_views.RoomDetailView.as_view(), name='room-detail'),

    path('faculty/allocate/', faculty_views.RoomAllocateView.as_view(), name='room-allocate'),
    path('faculty/allocations/<int:pk>/vacate/', faculty_views.RoomVacateView.as_view(), name='room-vacate'),

    path('faculty/violations/', faculty_views.ViolationListView.as_view(), name='violation-list'),
    path('faculty/violations/create/', faculty_views.ViolationCreateView.as_view(), name='violation-create'),
    path('faculty/violations/<int:pk>/', faculty_views.ViolationDetailView.as_view(), name='violation-detail'),

    # Student
    path('student/my-allocation/', student_views.StudentMyAllocationView.as_view(), name='student-my-allocation'),
    path('student/available-rooms/', student_views.StudentAvailableRoomsView.as_view(), name='student-available-rooms'),
    path('student/violations/', student_views.StudentViolationsView.as_view(), name='student-violations'),
]
