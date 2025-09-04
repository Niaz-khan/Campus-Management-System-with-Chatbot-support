from django.db import models

class DailySnapshot(models.Model):
    """Optional cached snapshot for quick dashboards."""
    date = models.DateField(unique=True)

    # Core counts
    total_students = models.PositiveIntegerField(default=0)
    total_faculty = models.PositiveIntegerField(default=0)
    total_enrollments = models.PositiveIntegerField(default=0)

    # Finance
    fees_collected = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fees_overdue = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Attendance & performance
    attendance_avg_percent = models.FloatField(default=0.0)
    avg_gpa = models.FloatField(default=0.0)

    # Utilization (optional)
    hostel_occupancy_percent = models.FloatField(default=0.0)
    cafeteria_active_subscriptions = models.PositiveIntegerField(default=0)
    transport_active_passes = models.PositiveIntegerField(default=0)
    sports_active_memberships = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Snapshot {self.date}"
