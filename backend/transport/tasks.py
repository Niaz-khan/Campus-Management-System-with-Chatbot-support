from datetime import date, timedelta
from .models import TransportPass
from notifications.utils import send_notification

def send_pass_expiry_reminders(days_before=7):
    today = date.today()
    expiry_date = today + timedelta(days=days_before)
    passes = TransportPass.objects.filter(is_active=True, end_date=expiry_date)
    for p in passes:
        send_notification(
            user=p.student.user,
            title="Transport Pass Expiry Reminder",
            message=f"Your transport pass will expire on {p.end_date}. Please renew if needed.",
            notification_type="REMINDER",
            related_object=p
        )
