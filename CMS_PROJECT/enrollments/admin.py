from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """
    Admin interface for managing student enrollments in courses.
    Allows admins to view, add, edit, and delete enrollments.
    """
    list_display = ('student', 'course', 'enrolled_on')
    search_fields = ('student__roll_number', 'course__course_code')
    list_filter = ('course',)