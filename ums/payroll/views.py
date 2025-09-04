from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.utils import timezone
import csv
from .models import EmployeeProfile, SalaryComponent, EmployeeSalaryTemplate, EmployeeSalaryComponent, PayrollRun, Payslip
from .serializers import (
    EmployeeProfileSerializer, SalaryComponentSerializer, EmployeeSalaryTemplateSerializer,
    EmployeeSalaryComponentSerializer, PayrollRunSerializer, PayslipSerializer
)
from .permissions import IsHR, IsPayrollViewer
from .utils import generate_payslip
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()


# Employee endpoints (HR)
class EmployeeProfileListCreateView(generics.ListCreateAPIView):
    queryset = EmployeeProfile.objects.select_related('user').all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [IsHR]

class EmployeeProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeeProfile.objects.select_related('user').all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [IsHR]


# Salary components CRUD
class SalaryComponentListCreateView(generics.ListCreateAPIView):
    queryset = SalaryComponent.objects.all()
    serializer_class = SalaryComponentSerializer
    permission_classes = [IsHR]

class SalaryComponentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SalaryComponent.objects.all()
    serializer_class = SalaryComponentSerializer
    permission_classes = [IsHR]


# Salary template endpoints
class EmployeeSalaryTemplateView(generics.RetrieveUpdateAPIView):
    queryset = EmployeeSalaryTemplate.objects.select_related('employee').all()
    serializer_class = EmployeeSalaryTemplateSerializer
    permission_classes = [IsHR]

# EmployeeSalaryComponent create / update
class EmployeeSalaryComponentCreateView(generics.CreateAPIView):
    queryset = EmployeeSalaryComponent.objects.all()
    serializer_class = EmployeeSalaryComponentSerializer
    permission_classes = [IsHR]


# Payroll Run management
class PayrollRunListCreateView(generics.ListCreateAPIView):
    queryset = PayrollRun.objects.all()
    serializer_class = PayrollRunSerializer
    permission_classes = [IsHR]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PayrollRunDetailView(generics.RetrieveUpdateAPIView):
    queryset = PayrollRun.objects.all()
    serializer_class = PayrollRunSerializer
    permission_classes = [IsHR]


# Trigger payroll generation for a run (generate payslips)
class PayrollProcessView(views.APIView):
    permission_classes = [IsHR]

    @transaction.atomic
    def post(self, request, pk):
        payroll_run = PayrollRun.objects.get(pk=pk)
        if payroll_run.status not in ('DRAFT','CANCELLED'):
            return Response({"detail":"Payroll already processed or processing."}, status=status.HTTP_400_BAD_REQUEST)
        payroll_run.status = 'PROCESSING'
        payroll_run.save(update_fields=['status'])

        # Generate payslips for all active employees (or filtered)
        employees = EmployeeProfile.objects.filter(is_active=True)
        for emp in employees:
            generate_payslip(payroll_run, emp)

        payroll_run.status = 'COMPLETED'
        payroll_run.save(update_fields=['status'])
        return Response({"detail":"Payroll processed."})

# View payslips for HR or viewer
class PayslipListView(generics.ListAPIView):
    serializer_class = PayslipSerializer
    permission_classes = [IsPayrollViewer]

    def get_queryset(self):
        qs = Payslip.objects.select_related('employee','payroll_run').all()
        employee_id = self.request.query_params.get('employee')
        month = self.request.query_params.get('month')
        if employee_id:
            qs = qs.filter(employee__id=employee_id)
        if month:
            # parse YYYY-MM or YYYY-MM-DD allowed
            qs = qs.filter(payroll_run__month__year=int(month.split('-')[0]), payroll_run__month__month=int(month.split('-')[1]))
        return qs

class PayslipDetailView(generics.RetrieveAPIView):
    queryset = Payslip.objects.select_related('employee','payroll_run').all()
    serializer_class = PayslipSerializer
    permission_classes = [IsPayrollViewer]


# Export payslips CSV for a payroll run
class ExportPayslipsCSVView(views.APIView):
    permission_classes = [IsHR]

    def get(self, request, pk):
        run = PayrollRun.objects.get(pk=pk)
        payslips = Payslip.objects.filter(payroll_run=run).select_related('employee','employee__user')
        # stream CSV
        response = HttpResponse(content_type='text/csv')
        filename = f"payslips_{run.month.strftime('%Y_%m')}.csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        writer.writerow(['Employee ID','Name','Department','Designation','Gross','Deductions','Net','Processed','Processed At'])
        for p in payslips:
            writer.writerow([
                p.employee.employee_id,
                p.employee.user.get_full_name(),
                p.employee.department,
                p.employee.designation,
                str(p.gross_earnings),
                str(p.total_deductions),
                str(p.net_pay),
                'Yes' if p.processed else 'No',
                p.processed_at.isoformat() if p.processed_at else ''
            ])
        return response
