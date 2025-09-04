from django.shortcuts import render

# Create your views here.
import csv
from io import StringIO
from datetime import datetime
from django.http import HttpResponse
from rest_framework import views, generics, permissions, status
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from .permissions import IsAdmin, IsFaculty
from .serializers import AdminOverviewSerializer, FacultyOverviewSerializer, SnapshotSerializer
from .models import DailySnapshot
from .utils import admin_metrics, faculty_metrics

def _parse_filters(request):
    batch_id = request.query_params.get('batch_id')
    program_id = request.query_params.get('program_id')
    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to')
    return (
        {k:int(v) for k,v in {'batch_id':batch_id, 'program_id':program_id}.items() if v},
        parse_date(date_from) if date_from else None,
        parse_date(date_to) if date_to else None
    )

class AdminOverviewView(views.APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        filters, dfrom, dto = _parse_filters(request)
        data = admin_metrics(filters=filters, date_from=dfrom, date_to=dto)
        return Response(AdminOverviewSerializer(data).data)

class FacultyOverviewView(views.APIView):
    permission_classes = [IsFaculty]

    def get(self, request):
        filters, dfrom, dto = _parse_filters(request)
        data = faculty_metrics(request.user, filters=filters, date_from=dfrom, date_to=dto)
        return Response(FacultyOverviewSerializer(data).data)

class SnapshotListCreateView(generics.ListCreateAPIView):
    """List recent snapshots or create a new one (admin only)."""
    queryset = DailySnapshot.objects.all()
    serializer_class = SnapshotSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        # Build snapshot from live metrics
        data = admin_metrics()
        serializer.save(
            total_students=data['total_students'],
            total_faculty=data['total_faculty'],
            total_enrollments=data['total_enrollments'],
            fees_collected=data['fees_collected'],
            fees_overdue=data['fees_overdue'],
            attendance_avg_percent=data['attendance_avg_percent'],
            avg_gpa=data['avg_gpa'],
            hostel_occupancy_percent=data['hostel_occupancy_percent'],
            cafeteria_active_subscriptions=data['cafeteria_active_subscriptions'],
            transport_active_passes=data['transport_active_passes'],
            sports_active_memberships=data['sports_active_memberships'],
        )

class ExportCSVView(views.APIView):
    """Export admin overview to CSV with current filters."""
    permission_classes = [IsAdmin]

    def get(self, request):
        filters, dfrom, dto = _parse_filters(request)
        data = admin_metrics(filters=filters, date_from=dfrom, date_to=dto)

        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerow(['Metric','Value'])
        for k, v in data.items():
            writer.writerow([k, v])

        resp = HttpResponse(buffer.getvalue(), content_type='text/csv')
        ts = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        resp['Content-Disposition'] = f'attachment; filename="ums_analytics_{ts}.csv"'
        return resp
