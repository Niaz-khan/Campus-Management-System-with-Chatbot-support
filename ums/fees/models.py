from django.db import models
from django.conf import settings
from students.models import StudentProfile

class FeeCategory(models.Model):
    """
    Categories of fees (Tuition, Hostel, Transport, Library Fine, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_recurring = models.BooleanField(default=True)  # E.g., Tuition vs Fine

    def __str__(self):
        return self.name


class Invoice(models.Model):
    """
    Represents a bill issued to a student for a specific semester or purpose.
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="invoices")
    category = models.ForeignKey(FeeCategory, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)
    reference_number = models.CharField(max_length=50, unique=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    fine_percentage_per_day = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00,
        help_text="Daily fine percentage applied after due date."
    )
    
    fine_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00,
        help_text="Calculated overdue fine."
    )
    
    fine_applied = models.BooleanField(default=False)

    def calculate_fine(self):
        """
        Calculate fine based on overdue days and fine percentage.
        """
        from datetime import date
        if self.is_paid or self.due_date >= date.today():
            return 0.00

        overdue_days = (date.today() - self.due_date).days
        return (self.amount * (self.fine_percentage_per_day / 100)) * overdue_days

    def __str__(self):
        return f"Invoice {self.reference_number} - {self.student.roll_no} - {self.amount}"


class Payment(models.Model):
    """
    Payment record against an invoice.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, default="Manual")  # Can later add enums: Bank Transfer, Stripe, PayPal
    paid_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for {self.invoice.reference_number}"
