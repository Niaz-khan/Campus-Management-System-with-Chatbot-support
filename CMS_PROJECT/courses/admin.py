from django.contrib import admin
from .models import Program, Semester, Course

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('program_name', 'department', 'duration_years', 'total_credits')

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('program', 'semester_number')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'semester', 'credits')
    search_fields = ('course_code', 'course_name')
    list_filter = ('semester',)
