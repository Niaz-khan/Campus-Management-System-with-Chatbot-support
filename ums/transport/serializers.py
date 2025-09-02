from rest_framework import serializers
from .models import TransportRoute, Vehicle, TransportPass
from students.serializers import StudentProfileSerializer

class TransportRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportRoute
        fields = ['id', 'name', 'start_point', 'end_point', 'stops', 'is_active', 'created_at']
        read_only_fields = ['created_at']


class VehicleSerializer(serializers.ModelSerializer):
    route_name = serializers.CharField(source='route.name', read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'route', 'route_name', 'vehicle_number', 'vehicle_type',
                  'driver_name', 'driver_contact', 'capacity', 'current_passengers', 'is_active']


class TransportPassSerializer(serializers.ModelSerializer):
    student_details = StudentProfileSerializer(source='student', read_only=True)
    vehicle_number = serializers.CharField(source='vehicle.vehicle_number', read_only=True)
    issued_by_name = serializers.CharField(source='issued_by.get_full_name', read_only=True)

    class Meta:
        model = TransportPass
        fields = ['id', 'student', 'student_details',
                  'vehicle', 'vehicle_number',
                  'issued_by', 'issued_by_name',
                  'start_date', 'end_date', 'monthly_fee',
                  'is_active', 'notes', 'created_at']
        read_only_fields = ['issued_by', 'created_at']
