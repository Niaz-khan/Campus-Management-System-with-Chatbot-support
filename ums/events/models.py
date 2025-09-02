from django.db import models
from django.conf import settings
from students.models import StudentProfile
from django.utils import timezone

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('SEMINAR', 'Seminar'),
        ('WORKSHOP', 'Workshop'),
        ('SPORTS', 'Sports'),
        ('CULTURAL', 'Cultural'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='OTHER')
    venue = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} – {self.date}"


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="event_registrations")
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    certificate_issued = models.BooleanField(default=False)

    class Meta:
        unique_together = ('event', 'student')

    def __str__(self):
        return f"{self.student.roll_no} – {self.event.title}"


class EventCertificate(models.Model):
    registration = models.OneToOneField(EventRegistration, on_delete=models.CASCADE, related_name="certificate")
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    issued_at = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to="certificates/events/", blank=True, null=True)

    def __str__(self):
        return f"Certificate – {self.registration.event.title} – {self.registration.student.roll_no}"
