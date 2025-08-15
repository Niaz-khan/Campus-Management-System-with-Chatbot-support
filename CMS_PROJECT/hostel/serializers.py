from rest_framework import serializers
from .models import (
    Hostel, Room, Student, Staff, Maintenance, Visitor,
    Complaint, Payment, Notice
)

class HostelSerializer(serializers.ModelSerializer):
    available_capacity = serializers.IntegerField(read_only=True)
    occupancy_rate = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    rooms_count = serializers.SerializerMethodField()
    staff_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Hostel
        fields = [
            'id', 'name', 'hostel_type', 'address', 'phone', 'email', 'capacity',
            'occupied', 'available_capacity', 'occupancy_rate', 'warden_name',
            'warden_phone', 'warden_email', 'description', 'amenities', 'rules',
            'monthly_rent', 'security_deposit', 'is_active', 'rooms_count',
            'staff_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['occupied', 'available_capacity', 'occupancy_rate', 'created_at', 'updated_at']
    
    def get_rooms_count(self, obj):
        return obj.rooms.count()
    
    def get_staff_count(self, obj):
        return obj.staff.filter(is_active=True).count()

class RoomSerializer(serializers.ModelSerializer):
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    available_beds = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Room
        fields = [
            'id', 'hostel', 'hostel_name', 'room_number', 'room_type', 'floor',
            'capacity', 'occupied', 'available_beds', 'is_full', 'status',
            'monthly_rent', 'description', 'amenities', 'is_ac',
            'is_attached_bathroom', 'students_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['occupied', 'available_beds', 'is_full', 'created_at', 'updated_at']
    
    def get_students_count(self, obj):
        return obj.students.filter(is_active=True).count()

class StudentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    room_info = serializers.CharField(source='room.__str__', read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'user', 'user_name', 'user_email', 'hostel', 'hostel_name',
            'room', 'room_info', 'student_id', 'check_in_date', 'check_out_date',
            'monthly_rent', 'security_deposit', 'emergency_contact_name',
            'emergency_contact_phone', 'emergency_contact_relationship',
            'medical_conditions', 'dietary_restrictions', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class StaffSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    staff_type_display = serializers.CharField(source='get_staff_type_display', read_only=True)
    
    class Meta:
        model = Staff
        fields = [
            'id', 'user', 'user_name', 'user_email', 'hostel', 'hostel_name',
            'staff_type', 'staff_type_display', 'employee_id', 'hire_date',
            'salary', 'phone', 'address', 'emergency_contact',
            'emergency_contact_phone', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class MaintenanceSerializer(serializers.ModelSerializer):
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    room_info = serializers.CharField(source='room.__str__', read_only=True)
    reported_by_name = serializers.CharField(source='reported_by.get_full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.user.get_full_name', read_only=True)
    maintenance_type_display = serializers.CharField(source='get_maintenance_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    days_overdue = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Maintenance
        fields = [
            'id', 'hostel', 'hostel_name', 'room', 'room_info', 'reported_by',
            'reported_by_name', 'maintenance_type', 'maintenance_type_display',
            'priority', 'priority_display', 'status', 'status_display', 'title',
            'description', 'reported_date', 'scheduled_date', 'completed_date',
            'assigned_to', 'assigned_to_name', 'estimated_cost', 'actual_cost',
            'notes', 'is_overdue', 'days_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['reported_date', 'is_overdue', 'days_overdue', 'created_at', 'updated_at']

class VisitorSerializer(serializers.ModelSerializer):
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    visitor_type_display = serializers.CharField(source='get_visitor_type_display', read_only=True)
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Visitor
        fields = [
            'id', 'hostel', 'hostel_name', 'student', 'student_name',
            'visitor_name', 'visitor_type', 'visitor_type_display', 'phone',
            'id_proof_type', 'id_proof_number', 'purpose', 'check_in_time',
            'check_out_time', 'is_inside', 'notes', 'duration', 'created_at'
        ]
        read_only_fields = ['check_in_time', 'duration', 'created_at']
    
    def get_duration(self, obj):
        if obj.check_out_time:
            return str(obj.check_out_time - obj.check_in_time)
        return str(obj.duration)

class ComplaintSerializer(serializers.ModelSerializer):
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.user.get_full_name', read_only=True)
    complaint_type_display = serializers.CharField(source='get_complaint_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Complaint
        fields = [
            'id', 'hostel', 'hostel_name', 'student', 'student_name',
            'complaint_type', 'complaint_type_display', 'priority',
            'priority_display', 'status', 'status_display', 'title',
            'description', 'reported_date', 'resolved_date', 'assigned_to',
            'assigned_to_name', 'resolution', 'is_anonymous', 'created_at', 'updated_at'
        ]
        read_only_fields = ['reported_date', 'created_at', 'updated_at']

class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    hostel_name = serializers.CharField(source='student.hostel.name', read_only=True)
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    days_overdue = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'student', 'student_name', 'hostel_name', 'payment_type',
            'payment_type_display', 'amount', 'due_date', 'paid_date',
            'payment_method', 'payment_method_display', 'status',
            'status_display', 'reference_number', 'notes', 'is_overdue',
            'days_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['is_overdue', 'days_overdue', 'created_at', 'updated_at']

class NoticeSerializer(serializers.ModelSerializer):
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    published_by_name = serializers.CharField(source='published_by.get_full_name', read_only=True)
    notice_type_display = serializers.CharField(source='get_notice_type_display', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Notice
        fields = [
            'id', 'hostel', 'hostel_name', 'title', 'content', 'notice_type',
            'notice_type_display', 'is_important', 'is_active', 'published_date',
            'expiry_date', 'published_by', 'published_by_name', 'is_expired',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['published_date', 'is_expired', 'created_at', 'updated_at']

# Specialized serializers for specific use cases
class HostelSummarySerializer(serializers.Serializer):
    total_hostels = serializers.IntegerField()
    active_hostels = serializers.IntegerField()
    total_capacity = serializers.IntegerField()
    total_occupied = serializers.IntegerField()
    average_occupancy_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    hostels_by_type = serializers.DictField()

class RoomSearchSerializer(serializers.Serializer):
    hostel_id = serializers.IntegerField(required=False)
    room_type = serializers.CharField(required=False)
    floor = serializers.IntegerField(required=False)
    available_only = serializers.BooleanField(default=True)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

class StudentSearchSerializer(serializers.Serializer):
    hostel_id = serializers.IntegerField(required=False)
    room_id = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)
    check_in_date_from = serializers.DateField(required=False)
    check_in_date_to = serializers.DateField(required=False)

class HostelAnalyticsSerializer(serializers.Serializer):
    occupancy_statistics = serializers.DictField()
    maintenance_statistics = serializers.DictField()
    complaint_statistics = serializers.DictField()
    payment_statistics = serializers.DictField()
    popular_amenities = serializers.ListField()
    top_complaints = serializers.ListField()
