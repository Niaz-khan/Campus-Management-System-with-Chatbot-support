from django.urls import path
from .views import (
    FeeCategoryListCreateView,
    InvoiceListCreateView, InvoiceDetailView,
    PaymentCreateView
)

from .views import (
    StudentFeeReportView,
    BatchFeeReportView,
    OverdueInvoicesReportView
)

urlpatterns += [
    path('reports/student/<int:student_id>/', StudentFeeReportView.as_view(), name='student-fee-report'),
    path('reports/batch/<int:batch_id>/', BatchFeeReportView.as_view(), name='batch-fee-report'),
    path('reports/overdue/', OverdueInvoicesReportView.as_view(), name='overdue-fee-report'),
    path('categories/', FeeCategoryListCreateView.as_view(), name='fee-category-list-create'),
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('payments/', PaymentCreateView.as_view(), name='payment-create'),
]
