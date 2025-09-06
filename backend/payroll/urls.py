from django.urls import path
from . import views

urlpatterns = [
    # Employees
    path('employees/', views.EmployeeProfileListCreateView.as_view(), name='payroll-employees-list-create'),
    path('employees/<int:pk>/', views.EmployeeProfileDetailView.as_view(), name='payroll-employees-detail'),

    # Salary components
    path('components/', views.SalaryComponentListCreateView.as_view(), name='payroll-components-list-create'),
    path('components/<int:pk>/', views.SalaryComponentDetailView.as_view(), name='payroll-components-detail'),

    # Templates & components
    path('templates/<int:pk>/', views.EmployeeSalaryTemplateView.as_view(), name='payroll-template-detail'),
    path('template-components/create/', views.EmployeeSalaryComponentCreateView.as_view(), name='payroll-template-component-create'),

    # Payroll runs
    path('runs/', views.PayrollRunListCreateView.as_view(), name='payroll-runs-list-create'),
    path('runs/<int:pk>/', views.PayrollRunDetailView.as_view(), name='payroll-runs-detail'),
    path('runs/<int:pk>/process/', views.PayrollProcessView.as_view(), name='payroll-runs-process'),

    # Payslips
    path('payslips/', views.PayslipListView.as_view(), name='payroll-payslips-list'),
    path('payslips/<int:pk>/', views.PayslipDetailView.as_view(), name='payroll-payslips-detail'),
    path('runs/<int:pk>/export/', views.ExportPayslipsCSVView.as_view(), name='payroll-runs-export'),
]
