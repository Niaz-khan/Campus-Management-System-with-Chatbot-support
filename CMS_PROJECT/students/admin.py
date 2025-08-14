from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'user', 'program', 'status', 'batch')
    search_fields = ('roll_number', 'user__username')
    list_filter = ('program', 'status', 'batch')
