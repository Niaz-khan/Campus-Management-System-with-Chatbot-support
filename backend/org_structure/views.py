from rest_framework import generics, permissions
from .models import Campus, Department, DepartmentRole, DepartmentMember
from .serializers import (
    CampusSerializer, DepartmentSerializer,
    DepartmentRoleSerializer, DepartmentMemberSerializer
)
from .permissions import CanManageMembers

class CampusListCreateView(generics.ListCreateAPIView):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
    permission_classes = [CanManageMembers]


class CampusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
    permission_classes = [CanManageMembers]


class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.select_related('campus').all()
    serializer_class = DepartmentSerializer
    permission_classes = [CanManageMembers]


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.select_related('campus').all()
    serializer_class = DepartmentSerializer
    permission_classes = [CanManageMembers]


class DepartmentRoleListView(generics.ListAPIView):
    queryset = DepartmentRole.objects.all()
    serializer_class = DepartmentRoleSerializer
    permission_classes = [permissions.IsAuthenticated]


class DepartmentMemberListCreateView(generics.ListCreateAPIView):
    queryset = DepartmentMember.objects.select_related('department','user','role').all()
    serializer_class = DepartmentMemberSerializer
    permission_classes = [CanManageMembers]


class DepartmentMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DepartmentMember.objects.select_related('department','user','role').all()
    serializer_class = DepartmentMemberSerializer
    permission_classes = [CanManageMembers]
