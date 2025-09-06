from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

# Employee / Staff
class EmployeeProfile(models.Model):
    ROLE_CHOICES = [
        ('ADMIN','Admin'),
        ('FACULTY','Faculty'),
        ('STAFF','Staff'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=150, blank=True, null=True)
    designation = models.CharField(max_length=150, blank=True, null=True)
    date_joined = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    bank_account = models.CharField(max_length=64, blank=True, null=True)
    bank_name = models.CharField(max_length=128, blank=True, null=True)
    ifsc = models.CharField(max_length=32, blank=True, null=True)
    tax_id = models.CharField(max_length=64, blank=True, null=True)  # e.g., tax number
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"


# Salary components (earnings/deductions)
class SalaryComponent(models.Model):
    COMPONENT_TYPE = [
        ('EARNING','Earning'),
        ('DEDUCTION','Deduction'),
    ]
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=30, unique=True)
    component_type = models.CharField(max_length=10, choices=COMPONENT_TYPE, default='EARNING')
    # default amount type: fixed or percentage of basic
    is_percentage = models.BooleanField(default=False)
    default_value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


# Employee salary template (which components apply to an employee)
class EmployeeSalaryTemplate(models.Model):
    employee = models.OneToOneField(EmployeeProfile, on_delete=models.CASCADE, related_name='salary_template')
    basic = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    components = models.ManyToManyField(SalaryComponent, through='EmployeeSalaryComponent')

    def __str__(self):
        return f"SalaryTemplate: {self.employee.employee_id}"


class EmployeeSalaryComponent(models.Model):
    template = models.ForeignKey(EmployeeSalaryTemplate, on_delete=models.CASCADE)
    component = models.ForeignKey(SalaryComponent, on_delete=models.CASCADE)
    # override default value (fixed amount or percent)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    # If True, 'value' represents percentage of basic; otherwise fixed amount
    is_percentage = models.BooleanField(default=False)

    class Meta:
        unique_together = ('template', 'component')

    def __str__(self):
        return f"{self.template.employee.employee_id} - {self.component.code}"


# Payroll run: monthly payroll grouping
class PayrollRun(models.Model):
    STATUS_CHOICES = [
        ('DRAFT','Draft'),
        ('PROCESSING','Processing'),
        ('COMPLETED','Completed'),
        ('CANCELLED','Cancelled'),
    ]

    month = models.DateField(help_text="Pick any date in the payroll month (e.g., 2025-09-01)")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('month',)

    def __str__(self):
        return f"Payroll {self.month.strftime('%Y-%m')}"


# Payslip for each employee under a payroll run
class Payslip(models.Model):
    payroll_run = models.ForeignKey(PayrollRun, on_delete=models.CASCADE, related_name='payslips')
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='payslips')
    gross_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    net_pay = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('payroll_run', 'employee')

    def __str__(self):
        return f"Payslip {self.employee.employee_id} [{self.payroll_run}]"
