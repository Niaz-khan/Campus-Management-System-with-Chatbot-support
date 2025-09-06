from datetime import date, timedelta
from .models import Invoice
from notifications.utils import send_notification

def send_due_date_reminders(days_before=3):
    reminder_date = date.today() + timedelta(days=days_before)
    invoices = Invoice.objects.filter(
        is_paid=False,
        due_date=reminder_date
    )
    for invoice in invoices:
        send_notification(
            user=invoice.student.user,
            title="Fee Due Reminder",
            message=f"Your invoice {invoice.reference_number} is due on {invoice.due_date}. Please pay {invoice.amount}.",
            notification_type="REMINDER",
            related_object=invoice
        )

def send_overdue_alerts():
    today = date.today()
    overdue_invoices = Invoice.objects.filter(
        is_paid=False,
        due_date__lt=today
    )
    for invoice in overdue_invoices:
        send_notification(
            user=invoice.student.user,
            title="Invoice Overdue",
            message=f"Your invoice {invoice.reference_number} is overdue since {invoice.due_date}. Outstanding amount: {invoice.amount}.",
            notification_type="ALERT",
            related_object=invoice
        )

def apply_overdue_fines():
    today = date.today()
    overdue_invoices = Invoice.objects.filter(
        is_paid=False,
        due_date__lt=today
    )
    for invoice in overdue_invoices:
        fine = invoice.calculate_fine()
        if fine > 0:
            invoice.fine_amount = fine
            invoice.fine_applied = True
            invoice.save(update_fields=['fine_amount', 'fine_applied'])

            # Send notification
            send_notification(
                user=invoice.student.user,
                title="Overdue Fine Applied",
                message=(
                    f"A fine of {fine} has been applied to your invoice "
                    f"{invoice.reference_number} due to overdue payment."
                ),
                notification_type="ALERT",
                related_object=invoice
            )