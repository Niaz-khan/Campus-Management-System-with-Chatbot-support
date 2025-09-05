from django.urls import path
from . import views

urlpatterns = [
    path('campuses/', views.CampusListCreateView.as_view(), name='campuses-list-create'),
    path('campuses/<int:pk>/', views.CampusDetailView.as_view(), name='campuses-detail'),
    path('departments/', views.DepartmentListCreateView.as_view(), name='departments-list-create'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='departments-detail'),
    path('roles/', views.DepartmentRoleListView.as_view(), name='department-roles'),
    path('members/', views.DepartmentMemberListCreateView.as_view(), name='department-members-list-create'),
    path('members/<int:pk>/', views.DepartmentMemberDetailView.as_view(), name='department-members-detail'),
]
