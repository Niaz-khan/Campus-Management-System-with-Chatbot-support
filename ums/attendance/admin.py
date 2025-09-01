from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "date", "status", "marked_by")
    list_filter = ("status", "date", "enrollment__course")
    search_fields = ("enrollment__student__roll_no", "enrollment__course__code")
