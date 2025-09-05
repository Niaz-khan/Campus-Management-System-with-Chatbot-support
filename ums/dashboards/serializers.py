from rest_framework import serializers

class AdminDashboardSerializer(serializers.Serializer):
    total_students = serializers.IntegerField()
    total_faculty = serializers.IntegerField()
    total_courses = serializers.IntegerField()
    fees_collected = serializers.DecimalField(max_digits=14, decimal_places=2)
    fees_overdue = serializers.DecimalField(max_digits=14, decimal_places=2)
    attendance_avg_percent = serializers.FloatField()
    upcoming_exams = serializers.IntegerField()
    unread_notifications = serializers.IntegerField()

class DepartmentDashboardSerializer(serializers.Serializer):
    students = serializers.IntegerField()
    faculty = serializers.IntegerField()
    courses = serializers.IntegerField()
    attendance_avg_percent = serializers.FloatField()
    upcoming_exams = serializers.IntegerField()
    unread_notifications = serializers.IntegerField()

class FacultyDashboardSerializer(serializers.Serializer):
    my_courses = serializers.IntegerField()
    to_mark_attendance = serializers.IntegerField()
    to_grade = serializers.IntegerField()
    unread_notifications = serializers.IntegerField()

class StudentDashboardSerializer(serializers.Serializer):
    enrolled_courses = serializers.IntegerField()
    upcoming_exams = serializers.IntegerField()
    attendance_percent = serializers.FloatField()
    fees_due = serializers.DecimalField(max_digits=12, decimal_places=2)
    unread_notifications = serializers.IntegerField()
