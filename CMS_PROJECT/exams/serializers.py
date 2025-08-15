from rest_framework import serializers
from .models import Exam, ExamSchedule, ExamResult, Grade, Transcript, ExamAttendance

class ExamSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.course_name', read_only=True)
    course_code = serializers.CharField(source='course.course_code', read_only=True)
    semester_info = serializers.CharField(source='semester.__str__', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    exam_type_display = serializers.CharField(source='get_exam_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Exam
        fields = [
            'id', 'title', 'exam_type', 'exam_type_display', 'course', 'course_name', 
            'course_code', 'semester', 'semester_info', 'total_marks', 'pass_marks',
            'duration_minutes', 'exam_date', 'start_time', 'end_time', 'venue',
            'instructions', 'status', 'status_display', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ExamScheduleSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    attendance_status_display = serializers.CharField(source='get_attendance_status_display', read_only=True)

    class Meta:
        model = ExamSchedule
        fields = [
            'id', 'student', 'student_name', 'student_roll', 'exam', 'exam_title',
            'is_eligible', 'attendance_status', 'attendance_status_display',
            'remarks', 'created_at'
        ]
        read_only_fields = ['created_at']

class ExamResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    course_code = serializers.CharField(source='exam.course.course_code', read_only=True)
    entered_by_name = serializers.CharField(source='entered_by.get_full_name', read_only=True)

    class Meta:
        model = ExamResult
        fields = [
            'id', 'student', 'student_name', 'student_roll', 'exam', 'exam_title',
            'course_code', 'marks_obtained', 'percentage', 'grade', 'grade_points',
            'remarks', 'entered_by', 'entered_by_name', 'entered_at', 'updated_at'
        ]
        read_only_fields = ['percentage', 'grade', 'grade_points', 'entered_at', 'updated_at']

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = [
            'id', 'grade', 'description', 'min_percentage', 'max_percentage',
            'grade_points', 'is_pass', 'remarks'
        ]

class TranscriptSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    semester_info = serializers.CharField(source='semester.__str__', read_only=True)
    academic_status_display = serializers.CharField(source='get_academic_status_display', read_only=True)
    generated_by_name = serializers.CharField(source='generated_by.get_full_name', read_only=True)

    class Meta:
        model = Transcript
        fields = [
            'id', 'student', 'student_name', 'student_roll', 'semester', 'semester_info',
            'total_credits', 'earned_credits', 'gpa', 'cgpa', 'academic_status',
            'academic_status_display', 'generated_at', 'generated_by', 'generated_by_name'
        ]
        read_only_fields = ['generated_at']

class ExamAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    recorded_by_name = serializers.CharField(source='recorded_by.get_full_name', read_only=True)

    class Meta:
        model = ExamAttendance
        fields = [
            'id', 'student', 'student_name', 'student_roll', 'exam', 'exam_title',
            'check_in_time', 'check_out_time', 'is_late', 'late_minutes',
            'supervisor_remarks', 'recorded_by', 'recorded_by_name', 'recorded_at'
        ]
        read_only_fields = ['recorded_at']

class StudentExamSummarySerializer(serializers.Serializer):
    """Serializer for student exam summary"""
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    semester = serializers.CharField()
    total_exams = serializers.IntegerField()
    exams_attended = serializers.IntegerField()
    exams_absent = serializers.IntegerField()
    total_marks = serializers.DecimalField(max_digits=8, decimal_places=2)
    average_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    gpa = serializers.DecimalField(max_digits=3, decimal_places=2)
    academic_status = serializers.CharField()

class ExamAnalyticsSerializer(serializers.Serializer):
    """Serializer for exam analytics"""
    exam_id = serializers.IntegerField()
    exam_title = serializers.CharField()
    total_students = serializers.IntegerField()
    present_students = serializers.IntegerField()
    absent_students = serializers.IntegerField()
    late_students = serializers.IntegerField()
    average_marks = serializers.DecimalField(max_digits=5, decimal_places=2)
    pass_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    highest_marks = serializers.DecimalField(max_digits=5, decimal_places=2)
    lowest_marks = serializers.DecimalField(max_digits=5, decimal_places=2)
