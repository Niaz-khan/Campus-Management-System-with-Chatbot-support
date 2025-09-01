from datetime import date, timedelta
from django.conf import settings
from .models import RoomAllocation
from notifications.utils import send_notification

# send reminder X days before allocation end
ALLOCATION_END_REMINDER_DAYS = getattr(settings, 'ALLOCATION_END_REMINDER_DAYS', 7)

def send_allocation_end_reminders():
    today = date.today()
    remind_date = today + timedelta(days=ALLOCATION_END_REMINDER_DAYS)
    allocations = RoomAllocation.objects.filter(is_active=True, end_date__isnull=False, end_date=remind_date)
    for alloc in allocations:
        send_notification(
            user=alloc.student.user,
            title="Hostel Allocation Ending Soon",
            message=f"Your room allocation for {alloc.room} ends on {alloc.end_date}. Please contact hostel office to extend or vacate.",
            notification_type="REMINDER",
            related_object=alloc
        )

def check_vacancies_and_notify_admin():
    # optional: notify admin if vacancy below threshold
    threshold = getattr(settings, 'HOSTEL_VACANCY_ALERT_THRESHOLD', 2)
    from .models import Room
    hostels = Room.objects.values('hostel').annotate(vacancies=models.Count('id', filter=models.Q(current_occupancy__lt=models.F('capacity'))))
    # for brevity don't implement notifications here; you can expand to notify admins if vacancies low
