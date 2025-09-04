from django.contrib import admin
from .models import EmployeeProfile, SalaryComponent, EmployeeSalaryTemplate, EmployeeSalaryComponent, PayrollRun, Payslip

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('employee_id','user','designation','department','is_active')
    search_fields = ('employee_id','user__email','user__first_name','user__last_name')

@admin.register(SalaryComponent)
class SalaryComponentAdmin(admin.ModelAdmin):
    list_display = ('name','code','component_type','is_percentage','default_value','active')
    search_fields = ('name','code')

@admin.register(EmployeeSalaryTemplate)
class EmployeeSalaryTemplateAdmin(admin.ModelAdmin):
    list_display = ('employee','basic')

@admin.register(EmployeeSalaryComponent)
class EmployeeSalaryComponentAdmin(admin.ModelAdmin):
    list_display = ('template','component','value','is_percentage')

@admin.register(PayrollRun)
class PayrollRunAdmin(admin.ModelAdmin):
    list_display = ('month','status','created_by','created_at')

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ('payroll_run','employee','net_pay','processed')
    list_filter = ('processed',)
