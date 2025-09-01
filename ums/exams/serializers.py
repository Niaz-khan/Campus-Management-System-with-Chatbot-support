from rest_framework import serializers
from .models import Exam, Grade
from courses.serializers import CourseSerializer

class ExamSerializer(serializers.ModelSerializer):
    course_details = CourseSerializer(source='course', read_only=True)
    faculty_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = Exam
        fields = [
            'id', 'course', 'course_details',
            'title', 'exam_type', 'total_marks',
            'date', 'grading_deadline_days',
            'faculty_name'
        ]

class GradeSerializer(serializers.ModelSerializer):
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    student_roll = serializers.CharField(source='enrollment.student.roll_no', read_only=True)

    class Meta:
        model = Grade
        fields = [
            'id', 'exam', 'exam_title',
            'enrollment', 'student_roll',
            'marks_obtained', 'remarks'
        ]

    def validate(self, data):
        exam = data.get('exam') or self.instance.exam
        if not exam.can_edit_grades():
            raise serializers.ValidationError(
                "Cannot add/update grades. Either grading period expired or exam is locked/published."
            )
        return data
