from django.utils import timezone
from .models import DailySnapshot
from .utils import admin_metrics

def create_daily_snapshot():
    today = timezone.now().date()
    data = admin_metrics()
    DailySnapshot.objects.update_or_create(
        date=today,
        defaults=dict(
            total_students=data['total_students'],
            total_faculty=data['total_faculty'],
            total_enrollments=data['total_enrollments'],
            fees_collected=data['fees_collected'],
            fees_overdue=data['fees_overdue'],
            attendance_avg_percent=data['attendance_avg_percent'],
            avg_gpa=data['avg_gpa'],
            hostel_occupancy_percent=data['hostel_occupancy_percent'],
            cafeteria_active_subscriptions=data['cafeteria_active_subscriptions'],
            transport_active_passes=data['transport_active_passes'],
            sports_active_memberships=data['sports_active_memberships'],
        )
    )
