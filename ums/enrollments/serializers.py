from rest_framework import serializers
from .models import Enrollment
from students.serializers import StudentProfileSerializer
from courses.serializers import CourseSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    student_details = StudentProfileSerializer(source='student', read_only=True)
    course_details = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_details',
            'course', 'course_details',
            'enrollment_date', 'status', 'grade'
        ]
