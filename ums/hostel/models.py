from django.db import models
from django.conf import settings
from students.models import StudentProfile
from django.utils import timezone

class Hostel(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=255, blank=True, null=True)
    contact_no = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('TRIPLE', 'Triple'),
    ]

    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    number = models.CharField(max_length=50)  # e.g., A-101
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, default='DOUBLE')
    capacity = models.PositiveIntegerField(default=2)
    current_occupancy = models.PositiveIntegerField(default=0)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('hostel', 'number')

    def __str__(self):
        return f"{self.hostel.name} - {self.number}"

    def has_vacancy(self):
        return self.current_occupancy < self.capacity


class RoomAllocation(models.Model):
    """
    A student allocated to a room for a period.
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='hostel_allocations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='allocations')
    allocated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # null until checked-out
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['student', 'room']),
        ]

    def __str__(self):
        return f"{self.student.roll_no} -> {self.room}"


class HostelViolation(models.Model):
    """
    Records misconduct or rule violation for a student in hostel.
    """
    allocation = models.ForeignKey(RoomAllocation, on_delete=models.CASCADE, related_name='violations')
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    description = models.TextField()
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Violation: {self.allocation.student.roll_no} - {self.date}"
