from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from .models import TransportRoute, Vehicle, TransportPass
from .serializers import TransportRouteSerializer, VehicleSerializer, TransportPassSerializer
from notifications.utils import send_notification

# Permissions based on your user roles
class IsAdminOrFaculty(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ('ADMIN','FACULTY'))

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'STUDENT')


# -------- Faculty/Admin APIs --------

class RouteListCreateView(generics.ListCreateAPIView):
    serializer_class = TransportRouteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = TransportRoute.objects.select_related('campus').all()

        campus_id = self.request.query_params.get('campus_id')
        if campus_id:
            queryset = queryset.filter(campus_id=campus_id)

        # Department filtering is optional here unless you have dept-based transport control
        return queryset


class RouteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransportRoute.objects.all()
    serializer_class = TransportRouteSerializer
    permission_classes = [IsAdminOrFaculty]


class VehicleListCreateView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.select_related('route').all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminOrFaculty]


class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransportRouteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = TransportRoute.objects.select_related('campus').all()

        campus_id = self.request.query_params.get('campus_id')
        if campus_id:
            queryset = queryset.filter(campus_id=campus_id)

        # Department filtering is optional here unless you have dept-based transport control
        return queryset


class IssueTransportPassView(generics.CreateAPIView):
    queryset = TransportPass.objects.all()
    serializer_class = TransportPassSerializer
    permission_classes = [IsAdminOrFaculty]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        vehicle = Vehicle.objects.select_for_update().filter(id=data.get('vehicle'), is_active=True).first()
        if not vehicle or not vehicle.has_vacancy():
            return Response({"detail":"Vehicle not available or full."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        pass_obj = serializer.save(issued_by=request.user, is_active=True)

        vehicle.current_passengers += 1
        vehicle.save(update_fields=['current_passengers'])

        # Send notification
        send_notification(
            user=pass_obj.student.user,
            title="Transport Pass Issued",
            message=f"Your pass for {vehicle.vehicle_number} has been issued.",
            notification_type="INFO",
            related_object=pass_obj
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RevokeTransportPassView(generics.UpdateAPIView):
    queryset = TransportPass.objects.all()
    serializer_class = TransportPassSerializer
    permission_classes = [IsAdminOrFaculty]

    def update(self, request, *args, **kwargs):
        pass_obj = self.get_object()
        if not pass_obj.is_active:
            return Response({"detail": "Pass already inactive."}, status=status.HTTP_400_BAD_REQUEST)

        pass_obj.is_active = False
        pass_obj.end_date = request.data.get('end_date') or timezone.now().date()
        pass_obj.save(update_fields=['is_active', 'end_date'])

        vehicle = pass_obj.vehicle
        vehicle.current_passengers = max(0, vehicle.current_passengers - 1)
        vehicle.save(update_fields=['current_passengers'])

        send_notification(
            user=pass_obj.student.user,
            title="Transport Pass Revoked",
            message=f"Your transport pass has been revoked as of {pass_obj.end_date}.",
            notification_type="ALERT",
            related_object=pass_obj
        )

        return Response({"detail": "Pass revoked successfully."}, status=status.HTTP_200_OK)


# -------- Student APIs --------

class StudentMyTransportPassView(generics.RetrieveAPIView):
    serializer_class = TransportPassSerializer
    permission_classes = [IsStudent]

    def get_object(self):
        return TransportPass.objects.select_related('vehicle','student').filter(student__user=self.request.user, is_active=True).first()


class StudentAvailableRoutesView(generics.ListAPIView):
    serializer_class = TransportRouteSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return TransportRoute.objects.filter(is_active=True)
