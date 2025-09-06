from rest_framework import serializers
from .models import StudentProfile
from academics.serializers import BatchSerializer, ProgramSerializer

class StudentProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    batch_details = BatchSerializer(source='batch', read_only=True)
    program_details = ProgramSerializer(source='program', read_only=True)
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user_email', 'roll_no',
            'batch', 'batch_details',
            'program', 'program_details',
            'semester', 'section', 'admission_date',
            'gpa', 'cgpa',
            'campus_name', 'department_name',
        ]
