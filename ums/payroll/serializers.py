from rest_framework import serializers
from .models import (
    EmployeeProfile, SalaryComponent, EmployeeSalaryTemplate,
    EmployeeSalaryComponent, PayrollRun, Payslip
)
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = ['id','user','user_name','user_email','employee_id','department','designation','date_joined','bank_account','bank_name','ifsc','tax_id','is_active','created_at']
        read_only_fields = ['created_at']

class SalaryComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryComponent
        fields = ['id','name','code','component_type','is_percentage','default_value','description','active']

class EmployeeSalaryComponentSerializer(serializers.ModelSerializer):
    component = SalaryComponentSerializer(read_only=True)
    component_id = serializers.PrimaryKeyRelatedField(source='component', queryset=SalaryComponent.objects.all(), write_only=True)
    class Meta:
        model = EmployeeSalaryComponent
        fields = ['id','template','component','component_id','value','is_percentage']

class EmployeeSalaryTemplateSerializer(serializers.ModelSerializer):
    components = EmployeeSalaryComponentSerializer(source='employeesalarycomponent_set', many=True, read_only=True)
    class Meta:
        model = EmployeeSalaryTemplate
        fields = ['id','employee','basic','components']

class PayrollRunSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    class Meta:
        model = PayrollRun
        fields = ['id','month','created_by','created_by_name','created_at','status','notes']

class PayslipSerializer(serializers.ModelSerializer):
    employee_details = EmployeeProfileSerializer(source='employee', read_only=True)
    class Meta:
        model = Payslip
        fields = ['id','payroll_run','employee','employee_details','gross_earnings','total_deductions','net_pay','processed','processed_at','notes']
        read_only_fields = ['gross_earnings','total_deductions','net_pay','processed','processed_at']

