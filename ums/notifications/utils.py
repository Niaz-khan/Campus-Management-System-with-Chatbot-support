from .models import Notification

def send_notification(user, title, message, notification_type='INFO', related_object=None):
    """
    Send a notification to a specific user.
    related_object can be any model instance (Exam, Enrollment, Fee, etc.)
    """
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        related_object_type=related_object.__class__.__name__ if related_object else None,
        related_object_id=related_object.id if related_object else None
    )
