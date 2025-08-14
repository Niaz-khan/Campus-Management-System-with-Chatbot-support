from django.contrib import admin
from .models import AdmissionApplication

@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'program', 'status', 'applied_on')
    search_fields = ('student__roll_number', 'program__program_name')
    list_filter = ('status',)
    ordering = ('-applied_on',)
    date_hierarchy = 'applied_on'