from django.contrib import admin
from .models import Exam, Grade

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "exam_type", "date", "grading_deadline_days", "created_by")
    list_filter = ("exam_type", "course__program", "date")
    search_fields = ("title", "course__code")

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "exam", "marks_obtained")
    list_filter = ("exam__course",)
    search_fields = ("enrollment__student__roll_no", "exam__title")
