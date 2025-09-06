from rest_framework import serializers
from .models import Hostel, Room, RoomAllocation, HostelViolation
from students.serializers import StudentProfileSerializer

class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = ['id', 'name', 'location', 'contact_no', 'description', 'created_at']
        read_only_fields = ['created_at']


class RoomSerializer(serializers.ModelSerializer):
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    class Meta:
        model = Room
        fields = ['id', 'hostel', 'hostel_name', 'number', 'room_type', 'capacity', 'current_occupancy', 'monthly_fee', 'is_active']


class RoomAllocationSerializer(serializers.ModelSerializer):
    student_details = StudentProfileSerializer(source='student', read_only=True)
    room_details = RoomSerializer(source='room', read_only=True)
    allocated_by_name = serializers.CharField(source='allocated_by.get_full_name', read_only=True)

    class Meta:
        model = RoomAllocation
        fields = [
            'id', 'student', 'student_details',
            'room', 'room_details',
            'allocated_by', 'allocated_by_name',
            'start_date', 'end_date', 'is_active', 'notes', 'created_at'
        ]
        read_only_fields = ['allocated_by', 'created_at']


class HostelViolationSerializer(serializers.ModelSerializer):
    allocation_details = RoomAllocationSerializer(source='allocation', read_only=True)

    class Meta:
        model = HostelViolation
        fields = ['id', 'allocation', 'allocation_details', 'reported_by', 'date', 'description', 'fine_amount', 'is_resolved', 'created_at']
        read_only_fields = ['created_at']
