from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.apply_for_admission, name='apply_for_admission'),
    path('admin/applications/', views.view_applications, name='view_applications'),
]
