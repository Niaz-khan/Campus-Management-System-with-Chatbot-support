from rest_framework import serializers
from .models import ParentProfile, ParentStudentLink
from students.serializers import StudentProfileSerializer
from fees.models import Invoice
from attendance.models import Attendance
from exams.models import Grade
from notifications.models import Notification

class ParentProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = ParentProfile
        fields = ['id', 'user_email', 'user_name', 'phone', 'address', 'created_at']

class ParentStudentLinkSerializer(serializers.ModelSerializer):
    student_details = StudentProfileSerializer(source='student', read_only=True)

    class Meta:
        model = ParentStudentLink
        fields = ['id', 'parent', 'student', 'student_details', 'relation', 'linked_at']

class ParentDashboardSerializer(serializers.Serializer):
    student = StudentProfileSerializer()
    attendance_percentage = serializers.FloatField()
    total_fees_due = serializers.DecimalField(max_digits=10, decimal_places=2)
    latest_grades = serializers.ListField()
    unread_notifications = serializers.IntegerField()
