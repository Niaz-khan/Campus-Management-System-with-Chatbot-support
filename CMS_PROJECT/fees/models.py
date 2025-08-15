from django.db import models
from django.conf import settings
from decimal import Decimal

class FeeStructure(models.Model):
    """Fee structure for different programs and semesters"""
    program = models.ForeignKey('courses.Program', on_delete=models.CASCADE)
    semester = models.ForeignKey('courses.Semester', on_delete=models.CASCADE)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    lab_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    library_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    examination_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    other_fees = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    academic_year = models.CharField(max_length=9)  # e.g., "2024-2025"
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('program', 'semester', 'academic_year')
        ordering = ['program', 'semester', 'academic_year']

    def save(self, *args, **kwargs):
        # Auto-calculate total fee
        self.total_fee = (
            self.tuition_fee + self.lab_fee + self.library_fee + 
            self.examination_fee + self.other_fees
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.program} - Sem {self.semester.semester_number} ({self.academic_year})"

class FeeChallan(models.Model):
    """Individual fee challan for students"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    challan_number = models.CharField(max_length=20, unique=True)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['-issue_date']

    def save(self, *args, **kwargs):
        # Auto-calculate remaining amount
        self.remaining_amount = self.total_amount - self.paid_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Challan {self.challan_number} - {self.student}"

class Payment(models.Model):
    """Payment records for fee challans"""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online Payment'),
        ('cheque', 'Cheque'),
    ]

    challan = models.ForeignKey(FeeChallan, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True)
    receipt_number = models.CharField(max_length=20, unique=True)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment {self.receipt_number} - {self.challan}"

class Scholarship(models.Model):
    """Scholarship and fee waiver information"""
    SCHOLARSHIP_TYPE_CHOICES = [
        ('merit', 'Merit-based'),
        ('need', 'Need-based'),
        ('sports', 'Sports'),
        ('academic', 'Academic Excellence'),
        ('other', 'Other'),
    ]

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    scholarship_type = models.CharField(max_length=20, choices=SCHOLARSHIP_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    academic_year = models.CharField(max_length=9)
    semester = models.ForeignKey('courses.Semester', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    granted_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['-granted_date']

    def __str__(self):
        return f"{self.scholarship_type} - {self.student} ({self.academic_year})"
