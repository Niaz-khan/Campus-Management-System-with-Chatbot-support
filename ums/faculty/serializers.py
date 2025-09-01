from rest_framework import serializers
from .models import FacultyProfile

class FacultyProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = FacultyProfile
        fields = [
            'id', 'user', 'user_email', 'full_name',
            'designation', 'department', 'office_room',
            'contact_no', 'joining_date', 'is_active'
        ]
