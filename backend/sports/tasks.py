from datetime import date, timedelta
from django.conf import settings
from .models import GymMembership, EquipmentIssue
from notifications.utils import send_notification

def send_membership_expiry_reminders(days_before=7):
    today = date.today()
    remind_date = today + timedelta(days=days_before)
    expiring = GymMembership.objects.filter(is_active=True, end_date=remind_date)
    for m in expiring:
        send_notification(
            user=m.student.user,
            title="Gym Membership Expiry Reminder",
            message=f"Your gym membership for {m.facility.name} expires on {m.end_date}. Please renew.",
            notification_type="REMINDER",
            related_object=m
        )

def apply_equipment_overdue_fines():
    today = date.today()
    overdue = EquipmentIssue.objects.filter(returned=False, due_date__lt=today)
    fine_per_day = getattr(settings,'EQUIPMENT_FINE_PER_DAY', 5.00)
    for issue in overdue:
        overdue_days = (today - issue.due_date).days
        issue.overdue_fine = overdue_days * fine_per_day
        issue.save(update_fields=['overdue_fine'])
        send_notification(
            user=issue.issued_to.user,
            title="Equipment Overdue",
            message=f"{issue.equipment.name} overdue by {overdue_days} day(s). Fine: {issue.overdue_fine}",
            notification_type="ALERT",
            related_object=issue
        )
