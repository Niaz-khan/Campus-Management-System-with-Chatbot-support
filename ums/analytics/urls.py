from django.urls import path
from . import views

urlpatterns = [
    path('admin/overview/', views.AdminOverviewView.as_view(), name='analytics-admin-overview'),
    path('faculty/overview/', views.FacultyOverviewView.as_view(), name='analytics-faculty-overview'),
    path('snapshots/', views.SnapshotListCreateView.as_view(), name='analytics-snapshots'),
    path('export/csv/', views.ExportCSVView.as_view(), name='analytics-export-csv'),
]
