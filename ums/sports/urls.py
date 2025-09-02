from django.urls import path
from . import views

urlpatterns = [
    # Faculty/Admin
    path('faculty/facilities/', views.FacilityListCreateView.as_view(), name='facility-list-create'),
    path('faculty/facilities/<int:pk>/', views.FacilityDetailView.as_view(), name='facility-detail'),

    path('faculty/memberships/', views.GymMembershipListCreateView.as_view(), name='gym-membership-list-create'),

    path('faculty/equipment/', views.EquipmentListCreateView.as_view(), name='equipment-list-create'),
    path('faculty/equipment/<int:pk>/', views.EquipmentDetailView.as_view(), name='equipment-detail'),
    path('faculty/equipment/issue/', views.IssueEquipmentView.as_view(), name='equipment-issue'),
    path('faculty/equipment/<int:pk>/return/', views.ReturnEquipmentView.as_view(), name='equipment-return'),

    path('faculty/tournaments/', views.TournamentListCreateView.as_view(), name='tournament-list-create'),
    path('faculty/tournaments/<int:pk>/', views.TournamentDetailView.as_view(), name='tournament-detail'),
    path('faculty/tournaments/registrations/', views.TournamentRegistrationListView.as_view(), name='tournament-registrations'),

    # Student
    path('student/memberships/', views.StudentMyMembershipView.as_view(), name='student-memberships'),
    path('student/facilities/', views.StudentAvailableFacilitiesView.as_view(), name='student-facilities'),
    path('student/issues/', views.StudentIssueListView.as_view(), name='student-issues'),
    path('student/tournaments/', views.StudentAvailableTournamentsView.as_view(), name='student-tournaments'),
    path('student/tournaments/register/', views.StudentRegisterTournamentView.as_view(), name='student-tournament-register'),
]
