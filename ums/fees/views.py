from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import FeeCategory, Invoice, Payment
from .serializers import FeeCategorySerializer, InvoiceSerializer, PaymentSerializer
from users.permissions import IsAdmin, IsFaculty
from notifications.utils import send_notification
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, F
from students.models import StudentProfile
from programs.models import Batch


class StudentFeeReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        student = StudentProfile.objects.get(id=student_id)
        invoices = Invoice.objects.filter(student=student)

        total_amount = invoices.aggregate(total=Sum('amount'))['total'] or 0
        total_paid = sum([sum([p.amount for p in inv.payments.all()]) for inv in invoices])
        total_fine = invoices.aggregate(fine=Sum('fine_amount'))['fine'] or 0
        outstanding = total_amount + total_fine - total_paid

        data = {
            "student": student.user.username,
            "roll_no": student.roll_no,
            "total_invoiced": total_amount,
            "total_fines": total_fine,
            "total_paid": total_paid,
            "outstanding_balance": outstanding,
            "invoices": [
                {
                    "reference_number": inv.reference_number,
                    "amount": inv.amount,
                    "fine": inv.fine_amount,
                    "due_date": inv.due_date,
                    "is_paid": inv.is_paid
                } for inv in invoices
            ]
        }
        return Response(data)
        

class BatchFeeReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, batch_id):
        batch = Batch.objects.get(id=batch_id)
        invoices = Invoice.objects.filter(student__batch=batch)

        total_amount = invoices.aggregate(total=Sum('amount'))['total'] or 0
        total_fine = invoices.aggregate(fine=Sum('fine_amount'))['fine'] or 0
        total_paid = 0
        for inv in invoices:
            total_paid += sum([p.amount for p in inv.payments.all()])

        outstanding = total_amount + total_fine - total_paid

        return Response({
            "batch": batch.name,
            "total_invoiced": total_amount,
            "total_fines": total_fine,
            "total_paid": total_paid,
            "outstanding_balance": outstanding,
            "invoice_count": invoices.count()
        })
        

class OverdueInvoicesReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        overdue_invoices = Invoice.objects.filter(is_paid=False, due_date__lt=F('due_date'))

        data = [
            {
                "student": inv.student.user.username,
                "reference_number": inv.reference_number,
                "amount": inv.amount,
                "fine": inv.fine_amount,
                "due_date": inv.due_date
            } for inv in overdue_invoices
        ]
        return Response({"overdue_invoices": data})


# 1. Fee Category Views (Admin only)
class FeeCategoryListCreateView(generics.ListCreateAPIView):
    queryset = FeeCategory.objects.all()
    serializer_class = FeeCategorySerializer
    permission_classes = [IsAdmin]


# 2. Invoice Views
class InvoiceListCreateView(generics.ListCreateAPIView):
    """
    Admin/Faculty: Can create invoices
    Students: Can only view their own invoices
    """
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'FACULTY']:
            return Invoice.objects.all()
        return Invoice.objects.filter(student__user=user)

    def perform_create(self, serializer):
        invoice = serializer.save()
        # Send notification to the student
        send_notification(
            user=invoice.student.user,
            title="New Invoice Issued",
            message=f"An invoice of {invoice.amount} has been generated. Due date: {invoice.due_date}",
            notification_type="INFO",
            related_object=invoice
        )


class InvoiceDetailView(generics.RetrieveUpdateAPIView):
    """
    Admin/Faculty: Can update invoice details (e.g., due_date)
    Students: Can only view
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAdmin() or IsFaculty()]
        return [permissions.IsAuthenticated()]


# 3. Payment Views
class PaymentCreateView(generics.CreateAPIView):
    """
    Students: Can record payment (manual for now)
    Admin/Faculty: Can record payment on behalf of student
    """
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(paid_by=self.request.user)
        invoice = payment.invoice
        # If fully paid, mark invoice as paid
        total_paid = sum(p.amount for p in invoice.payments.all())
        if total_paid >= invoice.amount:
            invoice.is_paid = True
            invoice.paid_at = payment.created_at
            invoice.save(update_fields=['is_paid', 'paid_at'])

        # Notify the student
        send_notification(
            user=invoice.student.user,
            title="Payment Confirmation",
            message=f"Payment of {payment.amount} received for invoice {invoice.reference_number}.",
            notification_type="INFO",
            related_object=invoice
        )

