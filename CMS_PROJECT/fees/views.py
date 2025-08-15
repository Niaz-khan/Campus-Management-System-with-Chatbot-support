from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import date

from .models import FeeStructure, FeeChallan, Payment, Scholarship
from .serializers import (
    FeeStructureSerializer, FeeChallanSerializer, 
    PaymentSerializer, ScholarshipSerializer, FeeSummarySerializer
)

class FeeStructureViewSet(viewsets.ModelViewSet):
    """API endpoint for fee structure management"""
    queryset = FeeStructure.objects.select_related('program', 'semester').all()
    serializer_class = FeeStructureSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['program__program_name', 'academic_year', 'semester__semester_number']
    ordering_fields = ['academic_year', 'total_fee', 'created_at']

    @action(detail=False, methods=['get'])
    def active_structures(self, request):
        """Get all active fee structures"""
        active_structures = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_structures, many=True)
        return Response(serializer.data)

class FeeChallanViewSet(viewsets.ModelViewSet):
    """API endpoint for fee challan management"""
    queryset = FeeChallan.objects.select_related(
        'student__user', 'fee_structure__program', 'fee_structure__semester'
    ).all()
    serializer_class = FeeChallanSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'challan_number', 'student__user__first_name', 
        'student__user__last_name', 'student__roll_number'
    ]
    ordering_fields = ['issue_date', 'due_date', 'total_amount', 'status']

    @action(detail=False, methods=['get'])
    def overdue_challans(self, request):
        """Get all overdue challans"""
        today = date.today()
        overdue = self.queryset.filter(
            due_date__lt=today, 
            status='pending'
        ).update(status='overdue')
        
        overdue_challans = self.queryset.filter(status='overdue')
        serializer = self.get_serializer(overdue_challans, many=True)
        return Response({
            'overdue_count': overdue,
            'challans': serializer.data
        })

    @action(detail=False, methods=['get'])
    def student_challans(self, request):
        """Get challans for a specific student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        student_challans = self.queryset.filter(student_id=student_id)
        serializer = self.get_serializer(student_challans, many=True)
        return Response(serializer.data)

class PaymentViewSet(viewsets.ModelViewSet):
    """API endpoint for payment management"""
    queryset = Payment.objects.select_related(
        'challan__student__user', 'received_by'
    ).all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'receipt_number', 'transaction_id', 'challan__challan_number'
    ]
    ordering_fields = ['payment_date', 'amount', 'created_at']

    def perform_create(self, serializer):
        """Update challan status when payment is created"""
        payment = serializer.save()
        challan = payment.challan
        
        # Update challan paid amount
        challan.paid_amount = challan.payments.aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Update challan status
        if challan.paid_amount >= challan.total_amount:
            challan.status = 'paid'
        elif challan.paid_amount > 0:
            challan.status = 'partial'
        
        challan.save()

class ScholarshipViewSet(viewsets.ModelViewSet):
    """API endpoint for scholarship management"""
    queryset = Scholarship.objects.select_related(
        'student__user', 'semester__program'
    ).all()
    serializer_class = ScholarshipSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'student__user__first_name', 'student__user__last_name',
        'scholarship_type', 'academic_year'
    ]
    ordering_fields = ['granted_date', 'amount', 'academic_year']

    @action(detail=False, methods=['get'])
    def active_scholarships(self, request):
        """Get all active scholarships"""
        active_scholarships = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_scholarships, many=True)
        return Response(serializer.data)

class FeeSummaryViewSet(viewsets.ViewSet):
    """API endpoint for fee summary and analytics"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def student_summary(self, request):
        """Get comprehensive fee summary for a student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get student's challans
        challans = FeeChallan.objects.filter(student_id=student_id)
        total_fees = challans.aggregate(total=Sum('total_amount'))['total'] or 0
        total_paid = challans.aggregate(total=Sum('paid_amount'))['total'] or 0
        total_remaining = total_fees - total_paid

        # Get student's scholarships
        scholarships = Scholarship.objects.filter(
            student_id=student_id, 
            is_active=True
        )
        total_scholarships = scholarships.aggregate(total=Sum('amount'))['total'] or 0

        # Calculate net remaining after scholarships
        net_remaining = max(0, total_remaining - total_scholarships)

        # Count challan statuses
        overdue_challans = challans.filter(status='overdue').count()
        pending_challans = challans.filter(status='pending').count()

        summary_data = {
            'student_id': student_id,
            'student_name': challans.first().student.user.get_full_name() if challans.exists() else '',
            'total_fees': total_fees,
            'total_paid': total_paid,
            'total_remaining': total_remaining,
            'total_scholarships': total_scholarships,
            'net_remaining': net_remaining,
            'overdue_challans': overdue_challans,
            'pending_challans': pending_challans,
        }

        serializer = FeeSummarySerializer(summary_data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def department_summary(self, request):
        """Get fee summary for a department"""
        department_id = request.query_params.get('department_id')
        if not department_id:
            return Response(
                {'error': 'department_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get all students in the department
        from students.models import Student
        students = Student.objects.filter(program__department_id=department_id)
        
        total_students = students.count()
        total_fees = 0
        total_paid = 0
        total_remaining = 0

        for student in students:
            challans = FeeChallan.objects.filter(student=student)
            total_fees += challans.aggregate(total=Sum('total_amount'))['total'] or 0
            total_paid += challans.aggregate(total=Sum('paid_amount'))['total'] or 0

        total_remaining = total_fees - total_paid

        return Response({
            'department_id': department_id,
            'total_students': total_students,
            'total_fees': total_fees,
            'total_paid': total_paid,
            'total_remaining': total_remaining,
            'collection_rate': (total_paid / total_fees * 100) if total_fees > 0 else 0
        })
