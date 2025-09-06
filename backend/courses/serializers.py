from rest_framework import serializers
from .models import Course
from academics.serializers import ProgramSerializer, BatchSerializer

class CourseSerializer(serializers.ModelSerializer):
    program_details = ProgramSerializer(source='program', read_only=True)
    batch_details = BatchSerializer(source='batch', read_only=True)
    faculty_name = serializers.CharField(source='faculty.get_full_name', read_only=True)
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'code', 'name', 'description',
            'credits', 'semester', 'course_type',
            'program', 'program_details',
            'batch', 'batch_details',
            'faculty', 'faculty_name',
            'campus_name','department_name',
        ]
