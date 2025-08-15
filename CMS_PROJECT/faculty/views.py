from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Department, Faculty
from .serializers import DepartmentSerializer, FacultySerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, creating, updating departments.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code']

class FacultyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, creating, updating faculty members.
    """
    queryset = Faculty.objects.select_related('user', 'department').all()
    serializer_class = FacultySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'employee_id', 'user__first_name', 'user__last_name', 
        'department__name', 'designation'
    ]
    ordering_fields = ['employee_id', 'joining_date', 'designation']
