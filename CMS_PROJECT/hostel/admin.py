from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum
from .models import (
    Hostel, Room, Student, Staff, Maintenance, Visitor,
    Complaint, Payment, Notice
)

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['name', 'hostel_type', 'capacity', 'occupied', 'available_capacity_display', 'occupancy_rate_display', 'monthly_rent', 'is_active', 'rooms_count', 'staff_count']
    list_filter = ['hostel_type', 'is_active', 'created_at']
    search_fields = ['name', 'address', 'warden_name', 'warden_email']
    ordering = ['name']
    readonly_fields = ['occupied', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def available_capacity_display(self, obj):
        return obj.available_capacity
    available_capacity_display.short_description = 'Available'
    
    def occupancy_rate_display(self, obj):
        return f"{obj.occupancy_rate:.1f}%"
    occupancy_rate_display.short_description = 'Occupancy Rate'
    
    def rooms_count(self, obj):
        return obj.rooms.count()
    rooms_count.short_description = 'Rooms'
    
    def staff_count(self, obj):
        return obj.staff.filter(is_active=True).count()
    staff_count.short_description = 'Staff'
    
    fieldsets = (
        ('Basic Information', {'fields': ('name', 'hostel_type', 'address', 'phone', 'email')}),
        ('Capacity & Pricing', {'fields': ('capacity', 'monthly_rent', 'security_deposit')}),
        ('Management', {'fields': ('warden_name', 'warden_phone', 'warden_email')}),
        ('Details', {'fields': ('description', 'amenities', 'rules')}),
        ('Status', {'fields': ('is_active',)}),
        ('System Fields', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'hostel', 'room_type', 'floor', 'capacity', 'occupied', 'available_beds_display', 'status', 'monthly_rent', 'is_ac', 'is_attached_bathroom']
    list_filter = ['hostel', 'room_type', 'floor', 'status', 'is_ac', 'is_attached_bathroom']
    search_fields = ['room_number', 'hostel__name', 'description']
    ordering = ['hostel', 'floor', 'room_number']
    readonly_fields = ['occupied', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def available_beds_display(self, obj):
        return obj.available_beds
    available_beds_display.short_description = 'Available Beds'
    
    fieldsets = (
        ('Room Information', {'fields': ('hostel', 'room_number', 'room_type', 'floor')}),
        ('Capacity & Status', {'fields': ('capacity', 'occupied', 'status')}),
        ('Pricing', {'fields': ('monthly_rent',)}),
        ('Amenities', {'fields': ('is_ac', 'is_attached_bathroom', 'amenities')}),
        ('Details', {'fields': ('description',)}),
        ('System Fields', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'user_name', 'hostel', 'room_info', 'check_in_date', 'check_out_date', 'monthly_rent', 'is_active', 'emergency_contact']
    list_filter = ['hostel', 'is_active', 'check_in_date', 'check_out_date']
    search_fields = ['student_id', 'user__first_name', 'user__last_name', 'user__email']
    ordering = ['-check_in_date']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'check_in_date'
    
    def user_name(self, obj):
        return obj.user.get_full_name()
    user_name.short_description = 'Student Name'
    
    def room_info(self, obj):
        if obj.room:
            return f"{obj.room.hostel.name} - Room {obj.room.room_number}"
        return 'No Room Assigned'
    room_info.short_description = 'Room'
    
    def emergency_contact(self, obj):
        return f"{obj.emergency_contact_name} ({obj.emergency_contact_phone})"
    emergency_contact.short_description = 'Emergency Contact'
    
    fieldsets = (
        ('Student Information', {'fields': ('user', 'student_id', 'hostel', 'room')}),
        ('Dates', {'fields': ('check_in_date', 'check_out_date')}),
        ('Financial', {'fields': ('monthly_rent', 'security_deposit')}),
        ('Emergency Contact', {'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')}),
        ('Additional Information', {'fields': ('medical_conditions', 'dietary_restrictions')}),
        ('Status', {'fields': ('is_active',)}),
        ('System Fields', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user_name', 'hostel', 'staff_type', 'hire_date', 'salary', 'phone', 'is_active']
    list_filter = ['hostel', 'staff_type', 'is_active', 'hire_date']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'user__email']
    ordering = ['hostel', 'staff_type', 'user__first_name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'hire_date'
    
    def user_name(self, obj):
        return obj.user.get_full_name()
    user_name.short_description = 'Staff Name'
    
    fieldsets = (
        ('Staff Information', {'fields': ('user', 'hostel', 'staff_type', 'employee_id')}),
        ('Employment Details', {'fields': ('hire_date', 'salary')}),
        ('Contact Information', {'fields': ('phone', 'address')}),
        ('Emergency Contact', {'fields': ('emergency_contact', 'emergency_contact_phone')}),
        ('Status', {'fields': ('is_active',)}),
        ('System Fields', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['title', 'hostel', 'room_info', 'maintenance_type', 'priority', 'status', 'reported_by', 'assigned_to', 'reported_date', 'is_overdue_display']
    list_filter = ['hostel', 'maintenance_type', 'priority', 'status', 'reported_date']
    search_fields = ['title', 'description', 'hostel__name', 'room__room_number']
    ordering = ['-reported_date']
    readonly_fields = ['reported_date', 'is_overdue', 'days_overdue', 'created_at', 'updated_at']
    date_hierarchy = 'reported_date'
    
    def room_info(self, obj):
        if obj.room:
            return f"{obj.room.hostel.name} - Room {obj.room.room_number}"
        return 'General'
    room_info.short_description = 'Room'
    
    def is_overdue_display(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red; font-weight: bold;">{} days overdue</span>', obj.days_overdue)
        return 'On time'
    is_overdue_display.short_description = 'Overdue Status'
    
    fieldsets = (
        ('Maintenance Information', {'fields': ('hostel', 'room', 'title', 'description')}),
        ('Classification', {'fields': ('maintenance_type', 'priority', 'status')}),
        ('Scheduling', {'fields': ('scheduled_date', 'completed_date')}),
        ('Assignment', {'fields': ('reported_by', 'assigned_to')}),
        ('Costs', {'fields': ('estimated_cost', 'actual_cost', 'notes')}),
        ('System Fields', {'fields': ('reported_date', 'is_overdue', 'days_overdue', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['visitor_name', 'hostel', 'student_name', 'visitor_type', 'check_in_time', 'check_out_time', 'is_inside', 'duration_display']
    list_filter = ['hostel', 'visitor_type', 'is_inside', 'check_in_time']
    search_fields = ['visitor_name', 'student__user__first_name', 'student__user__last_name', 'phone']
    ordering = ['-check_in_time']
    readonly_fields = ['check_in_time', 'duration', 'created_at']
    date_hierarchy = 'check_in_time'
    
    def student_name(self, obj):
        return obj.student.user.get_full_name()
    student_name.short_description = 'Student'
    
    def duration_display(self, obj):
        return str(obj.duration)
    duration_display.short_description = 'Duration'
    
    fieldsets = (
        ('Visitor Information', {'fields': ('hostel', 'student', 'visitor_name', 'visitor_type')}),
        ('Contact & ID', {'fields': ('phone', 'id_proof_type', 'id_proof_number')}),
        ('Visit Details', {'fields': ('purpose', 'check_in_time', 'check_out_time', 'is_inside')}),
        ('Notes', {'fields': ('notes',)}),
        ('System Fields', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'hostel', 'student_name', 'complaint_type', 'priority', 'status', 'reported_date', 'assigned_to', 'is_anonymous']
    list_filter = ['hostel', 'complaint_type', 'priority', 'status', 'reported_date', 'is_anonymous']
    search_fields = ['title', 'description', 'student__user__first_name', 'student__user__last_name']
    ordering = ['-reported_date']
    readonly_fields = ['reported_date', 'created_at', 'updated_at']
    date_hierarchy = 'reported_date'
    
    def student_name(self, obj):
        if obj.is_anonymous:
            return 'Anonymous'
        return obj.student.user.get_full_name()
    student_name.short_description = 'Student'
    
    fieldsets = (
        ('Complaint Information', {'fields': ('hostel', 'student', 'title', 'description')}),
        ('Classification', {'fields': ('complaint_type', 'priority', 'status', 'is_anonymous')}),
        ('Resolution', {'fields': ('assigned_to', 'resolved_date', 'resolution')}),
        ('System Fields', {'fields': ('reported_date', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'hostel_name', 'payment_type', 'amount', 'due_date', 'paid_date', 'status', 'is_overdue_display', 'days_overdue']
    list_filter = ['payment_type', 'status', 'due_date', 'paid_date']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'reference_number']
    ordering = ['-due_date']
    readonly_fields = ['is_overdue', 'days_overdue', 'created_at', 'updated_at']
    date_hierarchy = 'due_date'
    
    def student_name(self, obj):
        return obj.student.user.get_full_name()
    student_name.short_description = 'Student'
    
    def hostel_name(self, obj):
        return obj.student.hostel.name
    hostel_name.short_description = 'Hostel'
    
    def is_overdue_display(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red; font-weight: bold;">Overdue</span>')
        return 'On time'
    is_overdue_display.short_description = 'Overdue Status'
    
    fieldsets = (
        ('Payment Information', {'fields': ('student', 'payment_type', 'amount', 'due_date')}),
        ('Payment Details', {'fields': ('paid_date', 'payment_method', 'reference_number', 'status')}),
        ('Notes', {'fields': ('notes',)}),
        ('System Fields', {'fields': ('is_overdue', 'days_overdue', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'hostel', 'notice_type', 'is_important', 'is_active', 'published_date', 'expiry_date', 'published_by', 'is_expired_display']
    list_filter = ['hostel', 'notice_type', 'is_important', 'is_active', 'published_date']
    search_fields = ['title', 'content', 'hostel__name']
    ordering = ['-published_date']
    readonly_fields = ['published_date', 'is_expired', 'created_at', 'updated_at']
    date_hierarchy = 'published_date'
    
    def is_expired_display(self, obj):
        if obj.is_expired:
            return format_html('<span style="color: red; font-weight: bold;">Expired</span>')
        return 'Active'
    is_expired_display.short_description = 'Expiry Status'
    
    fieldsets = (
        ('Notice Information', {'fields': ('hostel', 'title', 'content', 'notice_type')}),
        ('Settings', {'fields': ('is_important', 'is_active')}),
        ('Publishing', {'fields': ('published_by', 'published_date', 'expiry_date')}),
        ('System Fields', {'fields': ('is_expired', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

# Admin actions
@admin.action(description="Mark selected maintenance requests as completed")
def mark_maintenance_completed(modeladmin, request, queryset):
    from django.utils import timezone
    updated = queryset.filter(status__in=['pending', 'in_progress']).update(
        status='completed',
        completed_date=timezone.now()
    )
    modeladmin.message_user(request, f"{updated} maintenance requests marked as completed.")

@admin.action(description="Mark selected complaints as resolved")
def mark_complaints_resolved(modeladmin, request, queryset):
    from django.utils import timezone
    updated = queryset.filter(status__in=['open', 'in_progress']).update(
        status='resolved',
        resolved_date=timezone.now()
    )
    modeladmin.message_user(request, f"{updated} complaints marked as resolved.")

@admin.action(description="Mark selected payments as paid")
def mark_payments_paid(modeladmin, request, queryset):
    from datetime import date
    updated = queryset.filter(status='pending').update(
        status='paid',
        paid_date=date.today()
    )
    modeladmin.message_user(request, f"{updated} payments marked as paid.")

# Add actions to admin classes
MaintenanceAdmin.actions = [mark_maintenance_completed]
ComplaintAdmin.actions = [mark_complaints_resolved]
PaymentAdmin.actions = [mark_payments_paid]
