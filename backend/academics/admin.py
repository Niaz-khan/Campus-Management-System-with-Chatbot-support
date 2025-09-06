from django.contrib import admin
from .models import Batch, Program

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "is_active")
    list_filter = ("is_active", "start_date", "end_date")
    search_fields = ("name",)

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "batch", "duration_years", "total_semesters")
    list_filter = ("batch",)
    search_fields = ("name",)
