from decimal import Decimal
from django.utils import timezone
from .models import Payslip, EmployeeSalaryComponent, EmployeeSalaryTemplate, SalaryComponent

def compute_payslip_for_employee(template: EmployeeSalaryTemplate):
    """
    Compute gross, deductions and net pay for an employee from their template.
    Returns dict: {'gross':Decimal,'deductions':Decimal,'net':Decimal,'breakdown':[...] }
    """
    basic = template.basic or Decimal('0.00')
    gross = basic
    deductions = Decimal('0.00')
    breakdown = []

    # Gather components
    components = EmployeeSalaryComponent.objects.filter(template=template).select_related('component')
    for esc in components:
        comp = esc.component
        if esc.is_percentage:
            amount = (basic * esc.value) / Decimal('100.00')
        else:
            amount = esc.value

        if comp.component_type == 'EARNING':
            gross += amount
            breakdown.append({'type':'earning','code':comp.code,'name':comp.name,'amount':amount})
        else:
            deductions += amount
            breakdown.append({'type':'deduction','code':comp.code,'name':comp.name,'amount':amount})

    net = gross - deductions
    return {
        'gross': gross.quantize(Decimal('0.01')),
        'deductions': deductions.quantize(Decimal('0.01')),
        'net': net.quantize(Decimal('0.01')),
        'breakdown': breakdown
    }

def generate_payslip(payroll_run, employee_profile):
    """
    Create or update payslip object for employee in given payroll run.
    """
    template = getattr(employee_profile, 'salary_template', None)
    if not template:
        # create minimal payslip with zeroes
        payslip, created = Payslip.objects.update_or_create(
            payroll_run=payroll_run,
            employee=employee_profile,
            defaults={'gross_earnings':0,'total_deductions':0,'net_pay':0}
        )
        return payslip

    computed = compute_payslip_for_employee(template)
    payslip, created = Payslip.objects.update_or_create(
        payroll_run=payroll_run,
        employee=employee_profile,
        defaults={
            'gross_earnings': computed['gross'],
            'total_deductions': computed['deductions'],
            'net_pay': computed['net'],
        }
    )
    return payslip
