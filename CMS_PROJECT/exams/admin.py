from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Avg, Count, Sum
from .models import Exam, ExamSchedule, ExamResult, Grade, Transcript, ExamAttendance

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'course', 'semester', 'exam_type', 'exam_date', 
        'start_time', 'end_time', 'total_marks', 'status', 'created_by'
    ]
    list_filter = [
        'exam_type', 'status', 'exam_date', 'course', 'semester'
    ]
    search_fields = [
        'title', 'course__course_code', 'course__course_name', 'venue'
    ]
    ordering = ['-exam_date', '-start_time']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'exam_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'exam_type', 'course', 'semester', 'status')
        }),
        ('Exam Details', {
            'fields': ('total_marks', 'pass_marks', 'duration_minutes')
        }),
        ('Schedule', {
            'fields': ('exam_date', 'start_time', 'end_time', 'venue')
        }),
        ('Additional Information', {
            'fields': ('instructions', 'created_by')
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ExamSchedule)
class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'exam', 'is_eligible', 'attendance_status', 'created_at'
    ]
    list_filter = ['is_eligible', 'attendance_status', 'exam__exam_date']
    search_fields = [
        'student__user__first_name', 'student__user__last_name',
        'student__roll_number', 'exam__title'
    ]
    ordering = ['exam__exam_date', 'exam__start_time']
    readonly_fields = ['created_at']
    
    def student(self, obj):
        return obj.student.user.get_full_name()
    student.short_description = 'Student Name'
    
    def exam(self, obj):
        return obj.exam.title
    exam.short_description = 'Exam'

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'exam', 'marks_obtained', 'percentage', 'grade',
        'grade_points', 'entered_by', 'entered_at'
    ]
    list_filter = [
        'grade', 'exam__exam_type', 'exam__exam_date', 'entered_at'
    ]
    search_fields = [
        'student__user__first_name', 'student__user__last_name',
        'student__roll_number', 'exam__title'
    ]
    ordering = ['-entered_at']
    readonly_fields = ['percentage', 'grade', 'grade_points', 'entered_at', 'updated_at']
    date_hierarchy = 'entered_at'
    
    def student(self, obj):
        return obj.student.user.get_full_name()
    student.short_description = 'Student Name'
    
    def exam(self, obj):
        return obj.exam.title
    exam.short_description = 'Exam'
    
    fieldsets = (
        ('Result Information', {
            'fields': ('student', 'exam', 'marks_obtained', 'remarks')
        }),
        ('Calculated Fields', {
            'fields': ('percentage', 'grade', 'grade_points'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('entered_by', 'entered_at', 'updated_at')
        }),
    )

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = [
        'grade', 'description', 'min_percentage', 'max_percentage',
        'grade_points', 'is_pass'
    ]
    list_filter = ['is_pass', 'grade_points']
    search_fields = ['grade', 'description']
    ordering = ['grade_points']

@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'semester', 'total_credits', 'earned_credits',
        'gpa', 'cgpa', 'academic_status', 'generated_at'
    ]
    list_filter = [
        'academic_status', 'semester', 'generated_at'
    ]
    search_fields = [
        'student__user__first_name', 'student__user__last_name',
        'student__roll_number'
    ]
    ordering = ['-generated_at']
    readonly_fields = ['generated_at']
    date_hierarchy = 'generated_at'
    
    def student(self, obj):
        return obj.student.user.get_full_name()
    student.short_description = 'Student Name'

@admin.register(ExamAttendance)
class ExamAttendanceAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'exam', 'check_in_time', 'check_out_time',
        'is_late', 'late_minutes', 'recorded_by', 'recorded_at'
    ]
    list_filter = ['is_late', 'exam__exam_date', 'recorded_at']
    search_fields = [
        'student__user__first_name', 'student__user__last_name',
        'student__roll_number', 'exam__title'
    ]
    ordering = ['-recorded_at']
    readonly_fields = ['recorded_at']
    date_hierarchy = 'recorded_at'
    
    def student(self, obj):
        return obj.student.user.get_full_name()
    student.short_description = 'Student Name'
    
    def exam(self, obj):
        return obj.exam.title
    exam.short_description = 'Exam'

# Custom admin actions
@admin.action(description="Mark selected exams as published")
def mark_published(modeladmin, request, queryset):
    updated = queryset.update(status='published')
    modeladmin.message_user(request, f"{updated} exams marked as published.")

@admin.action(description="Generate exam analytics report")
def generate_exam_report(modeladmin, request, queryset):
    # This would generate a detailed exam analytics report
    pass

# Add actions to ExamAdmin
ExamAdmin.actions = [mark_published, generate_exam_report]
