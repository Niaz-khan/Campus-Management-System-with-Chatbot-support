from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "status", "enrollment_date", "grade")
    list_filter = ("status", "course__program", "course__batch")
    search_fields = ("student__roll_no", "course__code")
