from rest_framework import serializers
from .models import Attendance
from enrollments.serializers import EnrollmentSerializer

class AttendanceSerializer(serializers.ModelSerializer):
    enrollment_details = EnrollmentSerializer(source='enrollment', read_only=True)
    faculty_name = serializers.CharField(source='marked_by.get_full_name', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 'enrollment', 'enrollment_details',
            'date', 'status', 'remarks', 'faculty_name', 'created_at'
        ]
