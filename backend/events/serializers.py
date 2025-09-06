from rest_framework import serializers
from .models import Event, EventRegistration, EventCertificate
from students.serializers import StudentProfileSerializer

class EventSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'event_type', 'venue',
                  'date', 'start_time', 'end_time', 'capacity',
                  'created_by', 'created_by_name', 'is_active', 'created_at']
        read_only_fields = ['created_by', 'created_at']


class EventRegistrationSerializer(serializers.ModelSerializer):
    student_details = StudentProfileSerializer(source='student', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'event_title', 'student', 'student_details',
                  'registered_at', 'attended', 'certificate_issued']
        read_only_fields = ['registered_at', 'certificate_issued']


class EventCertificateSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='registration.event.title', read_only=True)
    student_roll_no = serializers.CharField(source='registration.student.roll_no', read_only=True)
    issued_by_name = serializers.CharField(source='issued_by.get_full_name', read_only=True)

    class Meta:
        model = EventCertificate
        fields = ['id', 'registration', 'event_title', 'student_roll_no',
                  'issued_by', 'issued_by_name', 'issued_at', 'file']
        read_only_fields = ['issued_at']
