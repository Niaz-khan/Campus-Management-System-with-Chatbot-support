from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from .models import Event, EventRegistration, EventCertificate
from .serializers import EventSerializer, EventRegistrationSerializer, EventCertificateSerializer
from notifications.utils import send_notification
from org_structure.models import DepartmentMember

class IsAdminOrFaculty(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ('ADMIN','FACULTY'))

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'STUDENT')


# Faculty/Admin APIs
class EventListCreateView(generics.ListCreateAPIView):
    """
    
    """
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Event.objects.select_related('campus', 'department').all()

        campus_id = self.request.query_params.get('campus_id')
        department_id = self.request.query_params.get('department_id')

        if campus_id:
            queryset = queryset.filter(campus_id=campus_id)
        if department_id:
            queryset = queryset.filter(department_id=department_id)

        user = self.request.user
        if hasattr(user, 'departmentmember'):
            member = DepartmentMember.objects.filter(user=user, is_active=True).first()
            if member and member.role.name in ['HOD', 'COORDINATOR']:
                queryset = queryset.filter(department=member.department)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrFaculty]


class IssueCertificateView(generics.CreateAPIView):
    queryset = EventCertificate.objects.all()
    serializer_class = EventCertificateSerializer
    permission_classes = [IsAdminOrFaculty]

    def create(self, request, *args, **kwargs):
        registration_id = request.data.get("registration")
        try:
            registration = EventRegistration.objects.get(id=registration_id, attended=True)
        except EventRegistration.DoesNotExist:
            return Response({"detail": "Valid attended registration required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        certificate = serializer.save(issued_by=request.user)

        registration.certificate_issued = True
        registration.save(update_fields=['certificate_issued'])

        send_notification(
            user=registration.student.user,
            title="Certificate Issued",
            message=f"Your certificate for {registration.event.title} has been issued.",
            notification_type="SUCCESS",
            related_object=certificate
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Student APIs
class AvailableEventsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        today = timezone.now().date()
        return Event.objects.filter(is_active=True, date__gte=today)


class RegisterEventView(generics.CreateAPIView):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsStudent]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['student'] = request.user.studentprofile.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        registration = serializer.save()

        send_notification(
            user=registration.student.user,
            title="Event Registration",
            message=f"You have successfully registered for {registration.event.title}.",
            notification_type="INFO",
            related_object=registration
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyEventRegistrationsView(generics.ListAPIView):
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return EventRegistration.objects.filter(student__user=self.request.user)
