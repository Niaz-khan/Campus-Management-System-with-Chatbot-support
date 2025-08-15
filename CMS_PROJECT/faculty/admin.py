from django.contrib import admin
from .models import Department, Faculty

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'description']
    search_fields = ['name', 'code']
    ordering = ['name']

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = [
        'employee_id', 'user', 'department', 'designation', 
        'status', 'joining_date'
    ]
    list_filter = ['department', 'designation', 'status', 'joining_date']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name']
    ordering = ['employee_id']
    date_hierarchy = 'joining_date'
