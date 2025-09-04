from .models import PayrollRun
from .utils import generate_payslip
from django.utils import timezone
from datetime import date
# Example: run monthly payroll on day X

def scheduled_monthly_payroll(process_day=1):
    today = timezone.now().date()
    # if today is process day
    if today.day != process_day:
        return
    # create payroll run for current month
    run_date = date(today.year, today.month, 1)
    run, created = PayrollRun.objects.get_or_create(month=run_date, defaults={'status':'DRAFT'})
    # Should be run by HR user via script or service account
    # Or call process view logic here (careful with permissions)
    # generate payslips for all employees
    for emp in EmployeeProfile.objects.filter(is_active=True):
        generate_payslip(run, emp)
    run.status = 'COMPLETED'
    run.save()
