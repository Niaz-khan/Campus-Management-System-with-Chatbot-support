from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from .models import FeeStructure, FeeChallan, Payment, Scholarship

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = [
        'program', 'semester', 'academic_year', 'total_fee', 
        'is_active', 'created_at'
    ]
    list_filter = ['program', 'semester', 'academic_year', 'is_active']
    search_fields = ['program__program_name', 'academic_year']
    ordering = ['program', 'semester', 'academic_year']
    readonly_fields = ['total_fee', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('program', 'semester', 'academic_year', 'is_active')
        }),
        ('Fee Breakdown', {
            'fields': ('tuition_fee', 'lab_fee', 'library_fee', 'examination_fee', 'other_fees')
        }),
        ('System Fields', {
            'fields': ('total_fee', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(FeeChallan)
class FeeChallanAdmin(admin.ModelAdmin):
    list_display = [
        'challan_number', 'student_name', 'program', 'semester',
        'total_amount', 'paid_amount', 'remaining_amount', 'status', 'due_date'
    ]
    list_filter = ['status', 'issue_date', 'due_date', 'fee_structure__program']
    search_fields = [
        'challan_number', 'student__user__first_name', 
        'student__user__last_name', 'student__roll_number'
    ]
    ordering = ['-issue_date']
    readonly_fields = ['issue_date', 'remaining_amount']
    date_hierarchy = 'issue_date'
    
    def student_name(self, obj):
        return obj.student.user.get_full_name()
    student_name.short_description = 'Student Name'
    
    def program(self, obj):
        return obj.fee_structure.program.program_name
    program.short_description = 'Program'
    
    def semester(self, obj):
        return f"Sem {obj.fee_structure.semester.semester_number}"
    semester.short_description = 'Semester'
    
    fieldsets = (
        ('Challan Information', {
            'fields': ('challan_number', 'student', 'fee_structure', 'issue_date', 'due_date')
        }),
        ('Amount Details', {
            'fields': ('total_amount', 'paid_amount', 'remaining_amount', 'status')
        }),
        ('Additional Information', {
            'fields': ('remarks',)
        }),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'receipt_number', 'student_name', 'challan_number', 'amount',
        'payment_method', 'payment_date', 'received_by'
    ]
    list_filter = ['payment_method', 'payment_date', 'received_by']
    search_fields = [
        'receipt_number', 'transaction_id', 'challan__challan_number'
    ]
    ordering = ['-payment_date']
    readonly_fields = ['created_at']
    date_hierarchy = 'payment_date'
    
    def student_name(self, obj):
        return obj.challan.student.user.get_full_name()
    student_name.short_description = 'Student Name'
    
    def challan_number(self, obj):
        return obj.challan.challan_number
    challan_number.short_description = 'Challan Number'
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('receipt_number', 'challan', 'amount', 'payment_date')
        }),
        ('Payment Method', {
            'fields': ('payment_method', 'transaction_id')
        }),
        ('Additional Information', {
            'fields': ('received_by', 'remarks', 'created_at')
        }),
    )

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = [
        'student_name', 'scholarship_type', 'amount', 'percentage',
        'academic_year', 'semester', 'is_active', 'granted_date'
    ]
    list_filter = [
        'scholarship_type', 'academic_year', 'is_active', 'granted_date'
    ]
    search_fields = [
        'student__user__first_name', 'student__user__last_name',
        'scholarship_type', 'academic_year'
    ]
    ordering = ['-granted_date']
    date_hierarchy = 'granted_date'
    
    def student_name(self, obj):
        return obj.student.user.get_full_name()
    student_name.short_description = 'Student Name'
    
    def semester(self, obj):
        return f"Sem {obj.semester.semester_number}"
    semester.short_description = 'Semester'
    
    fieldsets = (
        ('Scholarship Information', {
            'fields': ('student', 'scholarship_type', 'amount', 'percentage')
        }),
        ('Academic Details', {
            'fields': ('academic_year', 'semester', 'is_active')
        }),
        ('Date Information', {
            'fields': ('granted_date', 'expiry_date')
        }),
        ('Additional Information', {
            'fields': ('remarks',)
        }),
    )

# Custom admin actions
@admin.action(description="Mark selected challans as overdue")
def mark_overdue(modeladmin, request, queryset):
    from datetime import date
    today = date.today()
    updated = queryset.filter(due_date__lt=today, status='pending').update(status='overdue')
    modeladmin.message_user(request, f"{updated} challans marked as overdue.")

@admin.action(description="Generate fee summary report")
def generate_fee_summary(modeladmin, request, queryset):
    # This would generate a detailed fee summary report
    pass

# Add actions to FeeChallanAdmin
FeeChallanAdmin.actions = [mark_overdue, generate_fee_summary]
