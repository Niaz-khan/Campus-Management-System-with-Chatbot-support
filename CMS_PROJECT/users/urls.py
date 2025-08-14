from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('unauthorized/', views.unauthorized_view, name='unauthorized'),
]
