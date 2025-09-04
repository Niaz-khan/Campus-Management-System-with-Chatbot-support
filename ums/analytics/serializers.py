from rest_framework import serializers
from .models import DailySnapshot

class AdminOverviewSerializer(serializers.Serializer):
    # Summary cards
    total_students = serializers.IntegerField()
    total_faculty = serializers.IntegerField()
    total_enrollments = serializers.IntegerField()

    # Finance
    fees_collected = serializers.DecimalField(max_digits=12, decimal_places=2)
    fees_overdue = serializers.DecimalField(max_digits=12, decimal_places=2)

    # Attendance & performance
    attendance_avg_percent = serializers.FloatField()
    avg_gpa = serializers.FloatField()

    # Utilization
    hostel_occupancy_percent = serializers.FloatField()
    cafeteria_active_subscriptions = serializers.IntegerField()
    transport_active_passes = serializers.IntegerField()
    sports_active_memberships = serializers.IntegerField()

class FacultyOverviewSerializer(serializers.Serializer):
    # Scoped to faculty’s batches/courses
    my_students = serializers.IntegerField()
    my_enrollments = serializers.IntegerField()
    my_attendance_avg_percent = serializers.FloatField()
    my_avg_grade = serializers.FloatField()

class SnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySnapshot
        fields = '__all__'
