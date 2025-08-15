from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from .models import (
    Hostel, Room, Student, Staff, Maintenance, Visitor,
    Complaint, Payment, Notice
)
from .serializers import (
    HostelSerializer, RoomSerializer, StudentSerializer, StaffSerializer,
    MaintenanceSerializer, VisitorSerializer, ComplaintSerializer,
    PaymentSerializer, NoticeSerializer, HostelSummarySerializer,
    RoomSearchSerializer, StudentSearchSerializer, HostelAnalyticsSerializer
)

class HostelViewSet(viewsets.ModelViewSet):
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address', 'warden_name', 'description']
    ordering_fields = ['name', 'capacity', 'occupied', 'monthly_rent', 'created_at']

    @action(detail=False, methods=['get'])
    def available_hostels(self, request):
        """Get hostels with available capacity"""
        available = self.queryset.filter(is_active=True).exclude(occupied__gte=models.F('capacity'))
        serializer = self.get_serializer(available, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get hostels filtered by type"""
        hostel_type = request.query_params.get('type')
        if hostel_type:
            hostels = self.queryset.filter(hostel_type=hostel_type, is_active=True)
            serializer = self.get_serializer(hostels, many=True)
            return Response(serializer.data)
        return Response({'error': 'Type parameter required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def occupancy_details(self, request, pk=None):
        """Get detailed occupancy information for a specific hostel"""
        hostel = self.get_object()
        data = {
            'hostel_name': hostel.name,
            'total_capacity': hostel.capacity,
            'occupied': hostel.occupied,
            'available': hostel.available_capacity,
            'occupancy_rate': hostel.occupancy_rate,
            'rooms': hostel.rooms.count(),
            'active_students': hostel.students.filter(is_active=True).count(),
            'staff_count': hostel.staff.filter(is_active=True).count()
        }
        return Response(data)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related('hostel').all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['room_number', 'hostel__name', 'description']
    ordering_fields = ['room_number', 'floor', 'capacity', 'occupied', 'monthly_rent']

    @action(detail=False, methods=['get'])
    def available_rooms(self, request):
        """Get rooms with available beds"""
        available = self.queryset.filter(status='available').exclude(occupied__gte=models.F('capacity'))
        serializer = self.get_serializer(available, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_hostel(self, request):
        """Get rooms filtered by hostel"""
        hostel_id = request.query_params.get('hostel_id')
        if hostel_id:
            rooms = self.queryset.filter(hostel_id=hostel_id)
            serializer = self.get_serializer(rooms, many=True)
            return Response(serializer.data)
        return Response({'error': 'Hostel ID parameter required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def search_rooms(self, request):
        """Advanced room search with multiple filters"""
        hostel_id = request.query_params.get('hostel_id')
        room_type = request.query_params.get('room_type')
        floor = request.query_params.get('floor')
        available_only = request.query_params.get('available_only', 'true').lower() == 'true'
        max_price = request.query_params.get('max_price')
        
        queryset = self.queryset
        
        if hostel_id:
            queryset = queryset.filter(hostel_id=hostel_id)
        if room_type:
            queryset = queryset.filter(room_type=room_type)
        if floor:
            queryset = queryset.filter(floor=floor)
        if available_only:
            queryset = queryset.filter(status='available').exclude(occupied__gte=models.F('capacity'))
        if max_price:
            queryset = queryset.filter(monthly_rent__lte=max_price)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('user', 'hostel', 'room').all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student_id', 'user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['check_in_date', 'check_out_date', 'monthly_rent', 'created_at']

    @action(detail=False, methods=['get'])
    def active_students(self, request):
        """Get all active students"""
        active = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_hostel(self, request):
        """Get students filtered by hostel"""
        hostel_id = request.query_params.get('hostel_id')
        if hostel_id:
            students = self.queryset.filter(hostel_id=hostel_id)
            serializer = self.get_serializer(students, many=True)
            return Response(serializer.data)
        return Response({'error': 'Hostel ID parameter required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def check_out(self, request, pk=None):
        """Check out a student from hostel"""
        student = self.get_object()
        if not student.is_active:
            return Response({'error': 'Student is already checked out'}, status=status.HTTP_400_BAD_REQUEST)
        
        student.is_active = False
        student.check_out_date = date.today()
        student.save()
        
        serializer = self.get_serializer(student)
        return Response(serializer.data)

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.select_related('user', 'hostel').all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['hire_date', 'salary', 'created_at']

    @action(detail=False, methods=['get'])
    def active_staff(self, request):
        """Get all active staff members"""
        active = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get staff filtered by type"""
        staff_type = request.query_params.get('type')
        if staff_type:
            staff = self.queryset.filter(staff_type=staff_type, is_active=True)
            serializer = self.get_serializer(staff, many=True)
            return Response(serializer.data)
        return Response({'error': 'Type parameter required'}, status=status.HTTP_400_BAD_REQUEST)

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.select_related('hostel', 'room', 'reported_by', 'assigned_to').all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'hostel__name', 'room__room_number']
    ordering_fields = ['reported_date', 'scheduled_date', 'priority', 'status', 'created_at']

    @action(detail=False, methods=['get'])
    def pending_maintenance(self, request):
        """Get all pending maintenance requests"""
        pending = self.queryset.filter(status='pending')
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def overdue_maintenance(self, request):
        """Get overdue maintenance requests"""
        overdue = self.queryset.filter(status='pending').filter(scheduled_date__lt=timezone.now())
        serializer = self.get_serializer(overdue, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign_staff(self, request, pk=None):
        """Assign maintenance request to staff member"""
        maintenance = self.get_object()
        staff_id = request.data.get('staff_id')
        
        if not staff_id:
            return Response({'error': 'Staff ID required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            staff = Staff.objects.get(id=staff_id)
            maintenance.assigned_to = staff
            maintenance.status = 'in_progress'
            maintenance.save()
            
            serializer = self.get_serializer(maintenance)
            return Response(serializer.data)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff member not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark maintenance request as completed"""
        maintenance = self.get_object()
        actual_cost = request.data.get('actual_cost')
        notes = request.data.get('notes', '')
        
        maintenance.status = 'completed'
        maintenance.completed_date = timezone.now()
        if actual_cost:
            maintenance.actual_cost = actual_cost
        if notes:
            maintenance.notes = notes
        
        maintenance.save()
        
        serializer = self.get_serializer(maintenance)
        return Response(serializer.data)

class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.select_related('hostel', 'student').all()
    serializer_class = VisitorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['visitor_name', 'student__user__first_name', 'student__user__last_name']
    ordering_fields = ['check_in_time', 'check_out_time', 'created_at']

    @action(detail=False, methods=['get'])
    def current_visitors(self, request):
        """Get all current visitors (inside the hostel)"""
        current = self.queryset.filter(is_inside=True)
        serializer = self.get_serializer(current, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def check_out_visitor(self, request, pk=None):
        """Check out a visitor"""
        visitor = self.get_object()
        if not visitor.is_inside:
            return Response({'error': 'Visitor is already checked out'}, status=status.HTTP_400_BAD_REQUEST)
        
        visitor.is_inside = False
        visitor.check_out_time = timezone.now()
        visitor.save()
        
        serializer = self.get_serializer(visitor)
        return Response(serializer.data)

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.select_related('hostel', 'student', 'assigned_to').all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'student__user__first_name', 'student__user__last_name']
    ordering_fields = ['reported_date', 'priority', 'status', 'created_at']

    @action(detail=False, methods=['get'])
    def open_complaints(self, request):
        """Get all open complaints"""
        open_complaints = self.queryset.filter(status__in=['open', 'in_progress'])
        serializer = self.get_serializer(open_complaints, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def urgent_complaints(self, request):
        """Get urgent and high priority complaints"""
        urgent = self.queryset.filter(priority__in=['high', 'urgent'], status__in=['open', 'in_progress'])
        serializer = self.get_serializer(urgent, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign_staff(self, request, pk=None):
        """Assign complaint to staff member"""
        complaint = self.get_object()
        staff_id = request.data.get('staff_id')
        
        if not staff_id:
            return Response({'error': 'Staff ID required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            staff = Staff.objects.get(id=staff_id)
            complaint.assigned_to = staff
            complaint.status = 'in_progress'
            complaint.save()
            
            serializer = self.get_serializer(complaint)
            return Response(serializer.data)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff member not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def resolve_complaint(self, request, pk=None):
        """Resolve a complaint"""
        complaint = self.get_object()
        resolution = request.data.get('resolution', '')
        
        complaint.status = 'resolved'
        complaint.resolved_date = timezone.now()
        if resolution:
            complaint.resolution = resolution
        
        complaint.save()
        
        serializer = self.get_serializer(complaint)
        return Response(serializer.data)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('student', 'student__hostel').all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student__user__first_name', 'student__user__last_name', 'reference_number']
    ordering_fields = ['due_date', 'paid_date', 'amount', 'status', 'created_at']

    @action(detail=False, methods=['get'])
    def pending_payments(self, request):
        """Get all pending payments"""
        pending = self.queryset.filter(status='pending')
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def overdue_payments(self, request):
        """Get overdue payments"""
        overdue = self.queryset.filter(status='pending', due_date__lt=date.today())
        serializer = self.get_serializer(overdue, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Mark payment as paid"""
        payment = self.get_object()
        payment_method = request.data.get('payment_method', '')
        reference_number = request.data.get('reference_number', '')
        
        payment.status = 'paid'
        payment.paid_date = date.today()
        if payment_method:
            payment.payment_method = payment_method
        if reference_number:
            payment.reference_number = reference_number
        
        payment.save()
        
        serializer = self.get_serializer(payment)
        return Response(serializer.data)

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.select_related('hostel', 'published_by').all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'hostel__name']
    ordering_fields = ['published_date', 'expiry_date', 'is_important', 'created_at']

    @action(detail=False, methods=['get'])
    def active_notices(self, request):
        """Get all active notices"""
        active = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def important_notices(self, request):
        """Get important notices"""
        important = self.queryset.filter(is_important=True, is_active=True)
        serializer = self.get_serializer(important, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_hostel(self, request):
        """Get notices filtered by hostel"""
        hostel_id = request.query_params.get('hostel_id')
        if hostel_id:
            notices = self.queryset.filter(hostel_id=hostel_id, is_active=True)
            serializer = self.get_serializer(notices, many=True)
            return Response(serializer.data)
        return Response({'error': 'Hostel ID parameter required'}, status=status.HTTP_400_BAD_REQUEST)

class HostelAnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get comprehensive hostel dashboard statistics"""
        total_hostels = Hostel.objects.count()
        active_hostels = Hostel.objects.filter(is_active=True).count()
        total_capacity = Hostel.objects.aggregate(total=Sum('capacity'))['total'] or 0
        total_occupied = Hostel.objects.aggregate(total=Sum('occupied'))['total'] or 0
        
        # Calculate average occupancy rate
        if total_capacity > 0:
            average_occupancy_rate = (total_occupied / total_capacity) * 100
        else:
            average_occupancy_rate = 0
        
        # Hostels by type
        hostels_by_type = {}
        for hostel_type, _ in Hostel.HOSTEL_TYPE_CHOICES:
            count = Hostel.objects.filter(hostel_type=hostel_type, is_active=True).count()
            hostels_by_type[hostel_type] = count
        
        # Maintenance statistics
        maintenance_stats = {
            'total': Maintenance.objects.count(),
            'pending': Maintenance.objects.filter(status='pending').count(),
            'in_progress': Maintenance.objects.filter(status='in_progress').count(),
            'completed': Maintenance.objects.filter(status='completed').count(),
            'overdue': Maintenance.objects.filter(status='pending', scheduled_date__lt=timezone.now()).count()
        }
        
        # Complaint statistics
        complaint_stats = {
            'total': Complaint.objects.count(),
            'open': Complaint.objects.filter(status='open').count(),
            'in_progress': Complaint.objects.filter(status='in_progress').count(),
            'resolved': Complaint.objects.filter(status='resolved').count(),
            'urgent': Complaint.objects.filter(priority__in=['high', 'urgent'], status__in=['open', 'in_progress']).count()
        }
        
        # Payment statistics
        payment_stats = {
            'total_pending': Payment.objects.filter(status='pending').count(),
            'total_overdue': Payment.objects.filter(status='pending', due_date__lt=date.today()).count(),
            'total_amount_pending': Payment.objects.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0,
            'total_amount_overdue': Payment.objects.filter(status='pending', due_date__lt=date.today()).aggregate(total=Sum('amount'))['total'] or 0
        }
        
        analytics_data = {
            'total_hostels': total_hostels,
            'active_hostels': active_hostels,
            'total_capacity': total_capacity,
            'total_occupied': total_occupied,
            'average_occupancy_rate': round(average_occupancy_rate, 2),
            'hostels_by_type': hostels_by_type,
            'maintenance_statistics': maintenance_stats,
            'complaint_statistics': complaint_stats,
            'payment_statistics': payment_stats
        }
        
        serializer = HostelAnalyticsSerializer(analytics_data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def hostel_summary(self, request):
        """Get summary statistics for all hostels"""
        hostels = Hostel.objects.filter(is_active=True)
        summary_data = []
        
        for hostel in hostels:
            data = {
                'id': hostel.id,
                'name': hostel.name,
                'type': hostel.hostel_type,
                'capacity': hostel.capacity,
                'occupied': hostel.occupied,
                'available': hostel.available_capacity,
                'occupancy_rate': hostel.occupancy_rate,
                'rooms_count': hostel.rooms.count(),
                'active_students': hostel.students.filter(is_active=True).count(),
                'staff_count': hostel.staff.filter(is_active=True).count(),
                'pending_maintenance': hostel.maintenance_requests.filter(status='pending').count(),
                'open_complaints': hostel.complaints.filter(status__in=['open', 'in_progress']).count()
            }
            summary_data.append(data)
        
        return Response(summary_data)
