from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "program", "batch", "semester", "credits", "course_type", "faculty")
    list_filter = ("program", "batch", "semester", "course_type")
    search_fields = ("code", "name")
