from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer

from org_structure.models import DepartmentMember

class NotificationListView(generics.ListAPIView):
    """
    this class 
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Notification.objects.select_related('user').all()

        campus_id = self.request.query_params.get('campus_id')
        department_id = self.request.query_params.get('department_id')

        if campus_id:
            queryset = queryset.filter(user__student_profile__campus_id=campus_id) | \
                       queryset.filter(user__faculty_profile__campus_id=campus_id)
        if department_id:
            queryset = queryset.filter(user__student_profile__department_id=department_id) | \
                       queryset.filter(user__faculty_profile__department_id=department_id)

        user = self.request.user
        if hasattr(user, 'departmentmember'):
            member = DepartmentMember.objects.filter(user=user, is_active=True).first()
            if member and member.role.name in ['HOD', 'COORDINATOR']:
                queryset = queryset.filter(
                    user__student_profile__department=member.department
                ) | queryset.filter(
                    user__faculty_profile__department=member.department
                )

        return queryset

class MarkNotificationReadView(generics.UpdateAPIView):
    """
    PATCH: Mark a notification as read
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.get_object().user != self.request.user:
            raise PermissionError("You are not allowed to modify this notification.")
        serializer.save(is_read=True)
