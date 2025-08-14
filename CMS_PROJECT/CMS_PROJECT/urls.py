from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    path('users/', include('users.urls')),
    path('admissions/', include('admissions.urls')),
    path('students/', include('students.urls')),
    path('courses/', include('courses.urls')),
    path('exams/', include('exams.urls')),
    path('enrollments/', include('enrollments.urls')),
    
]
