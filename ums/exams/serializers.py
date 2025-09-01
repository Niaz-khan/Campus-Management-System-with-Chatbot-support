from rest_framework import serializers
from .models import Exam
from courses.serializers import CourseSerializer

class ExamSerializer(serializers.ModelSerializer):
    course_details = CourseSerializer(source='course', read_only=True)
    faculty_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = Exam
        fields = [
            'id', 'course', 'course_details',
            'title', 'exam_type', 'total_marks',
            'date', 'faculty_name'
        ]
