"""
URL configuration for ums project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="UMS API",
      default_version='v1',
      description="University Management System API documentation",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Users API
    path('api/users/', include('users.urls')),
    path('api/academics/', include('academics.urls')),
    
    path('api/students/', include('students.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/enrollments/', include('enrollments.urls')),

    path('api/faculty/', include('faculty.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/exams/', include('exams.urls')),

    path('api/notifications/', include('notifications.urls')),
    path('api/fees/', include('fees.urls')),
    path('api/library/', include('library.urls')),

    path('api/hostel/', include('hostel.urls')),
    path('api/transport/', include('transport.urls')),
    path('api/cafeteria/', include('cafeteria.urls')),

    path('api/events/', include('events.urls')),
    path('api/sports/', include('sports.urls')),
    path('api/parents/', include('parents.urls')),

    path('api/analytics/', include('analytics.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

