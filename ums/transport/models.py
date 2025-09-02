from django.db import models
from django.conf import settings
from students.models import StudentProfile
from django.utils import timezone

class TransportRoute(models.Model):
    name = models.CharField(max_length=150)
    start_point = models.CharField(max_length=255)
    end_point = models.CharField(max_length=255)
    stops = models.TextField(help_text="Comma-separated list of stops")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.start_point} → {self.end_point})"


class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('BUS', 'Bus'),
        ('VAN', 'Van'),
    ]

    route = models.ForeignKey(TransportRoute, on_delete=models.CASCADE, related_name="vehicles")
    vehicle_number = models.CharField(max_length=50, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES, default='BUS')
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=30)
    capacity = models.PositiveIntegerField()
    current_passengers = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.vehicle_number} ({self.route.name})"

    def has_vacancy(self):
        return self.current_passengers < self.capacity


class TransportPass(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="transport_passes")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="passes")
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'vehicle', 'start_date')

    def __str__(self):
        return f"{self.student.roll_no} – {self.vehicle.vehicle_number}"
