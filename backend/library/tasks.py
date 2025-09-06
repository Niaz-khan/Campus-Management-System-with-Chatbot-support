from datetime import date
from django.db import transaction
from .models import BookBorrow, BookFine
from notifications.utils import send_notification
from decimal import Decimal
from django.conf import settings

# Default policy: per-book-per-day fine percentage or fixed amount. We'll use fixed per-day amount stored in settings.
LIBRARY_FINE_PER_DAY = getattr(settings, 'LIBRARY_FINE_PER_DAY', Decimal('5.00'))  # currency units per day

def apply_library_fines():
    """
    This function should be scheduled daily (Celery Beat or cron).
    For each BookBorrow that is overdue and not yet returned, create/update a BookFine.
    """
    today = date.today()
    overdue_borrows = BookBorrow.objects.filter(is_returned=False, due_date__lt=today)

    for borrow in overdue_borrows:
        overdue_days = (today - borrow.due_date).days
        fine_amount = (Decimal(overdue_days) * LIBRARY_FINE_PER_DAY).quantize(Decimal('0.01'))

        with transaction.atomic():
            fine, created = BookFine.objects.get_or_create(borrow_record=borrow)
            # If waived, skip overriding
            if fine.waived:
                continue
            fine.fine_amount = fine_amount
            fine.is_paid = False
            fine.save(update_fields=['fine_amount', 'is_paid'])

            send_notification(
                user=borrow.student.user,
                title="Library Overdue Fine",
                message=f"Your borrowed book '{borrow.book.title}' is overdue by {overdue_days} day(s). Fine: {fine.fine_amount}",
                notification_type="ALERT",
                related_object=fine
            )
