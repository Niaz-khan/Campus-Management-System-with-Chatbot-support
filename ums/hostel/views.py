from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from .models import Hostel, Room, RoomAllocation, HostelViolation
from .serializers import HostelSerializer, RoomSerializer, RoomAllocationSerializer, HostelViolationSerializer
from .permissions import IsAdminOrHostelStaff
from notifications.utils import send_notification
from .permissions import IsStudent
# optional fees integration: import a helper to create invoices
# from fees.utils import create_invoice_for_hostel_allocation

# Hostels CRUD
class HostelListCreateView(generics.ListCreateAPIView):
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    permission_classes = [IsAdminOrHostelStaff]


class HostelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    permission_classes = [IsAdminOrHostelStaff]


# Rooms CRUD
class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.select_related('hostel').all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrHostelStaff]


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.select_related('hostel').all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrHostelStaff]


# Allocate a room to student
class RoomAllocateView(generics.CreateAPIView):
    queryset = RoomAllocation.objects.all()
    serializer_class = RoomAllocationSerializer
    permission_classes = [IsAdminOrHostelStaff]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        room_id = data.get('room')
        student_id = data.get('student')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        room = Room.objects.select_for_update().filter(id=room_id, is_active=True).first()
        if not room:
            return Response({"detail":"Room not found or inactive"}, status=status.HTTP_404_NOT_FOUND)
        if not room.has_vacancy():
            return Response({"detail":"Room has no vacancy"}, status=status.HTTP_400_BAD_REQUEST)

        # create allocation
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        allocation = serializer.save(allocated_by=request.user, is_active=True)

        # increment occupancy
        room.current_occupancy += 1
        room.save(update_fields=['current_occupancy'])

        # Optional: create invoice for the first month or whole period
        # try:
        #     create_invoice_for_hostel_allocation(allocation)
        # except Exception:
        #     pass

        # notify student
        send_notification(
            user=allocation.student.user,
            title="Hostel Room Allocated",
            message=f"You have been allocated {allocation.room}. Start: {allocation.start_date}.",
            notification_type="INFO",
            related_object=allocation
        )

        return Response(self.get_serializer(allocation).data, status=status.HTTP_201_CREATED)


# De-allocate (vacate) a room
class RoomVacateView(generics.UpdateAPIView):
    queryset = RoomAllocation.objects.all()
    serializer_class = RoomAllocationSerializer
    permission_classes = [IsAdminOrHostelStaff]

    def update(self, request, *args, **kwargs):
        allocation = self.get_object()
        if not allocation.is_active:
            return Response({"detail":"Allocation already inactive"}, status=status.HTTP_400_BAD_REQUEST)

        allocation.is_active = False
        allocation.end_date = request.data.get('end_date') or timezone.now().date()
        allocation.save(update_fields=['is_active', 'end_date'])

        # decrement room occupancy
        room = allocation.room
        room.current_occupancy = max(0, room.current_occupancy - 1)
        room.save(update_fields=['current_occupancy'])

        send_notification(
            user=allocation.student.user,
            title="Hostel Room Vacated",
            message=f"Your room {room} has been vacated on {allocation.end_date}.",
            notification_type="INFO",
            related_object=allocation
        )

        return Response({"detail":"Student vacated successfully."}, status=status.HTTP_200_OK)


# Violations
class ViolationCreateView(generics.CreateAPIView):
    queryset = HostelViolation.objects.all()
    serializer_class = HostelViolationSerializer
    permission_classes = [IsAdminOrHostelStaff]

    def perform_create(self, serializer):
        violation = serializer.save()
        # notify student
        send_notification(
            user=violation.allocation.student.user,
            title="Hostel Violation Reported",
            message=f"Violation reported on {violation.date}: {violation.description}",
            notification_type="ALERT",
            related_object=violation
        )


class ViolationListView(generics.ListAPIView):
    queryset = HostelViolation.objects.select_related('allocation__student','reported_by').all()
    serializer_class = HostelViolationSerializer
    permission_classes = [IsAdminOrHostelStaff]


class ViolationDetailView(generics.RetrieveUpdateAPIView):
    queryset = HostelViolation.objects.all()
    serializer_class = HostelViolationSerializer
    permission_classes = [IsAdminOrHostelStaff]


class StudentMyAllocationView(generics.RetrieveAPIView):
    serializer_class = RoomAllocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Return active allocation for current student if any
        return RoomAllocation.objects.select_related('room','student').filter(student__user=self.request.user, is_active=True).first()

class StudentAvailableRoomsView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # show rooms with vacancy
        return Room.objects.filter(is_active=True).filter(current_occupancy__lt=models.F('capacity'))

class StudentViolationsView(generics.ListAPIView):
    serializer_class = HostelViolationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HostelViolation.objects.filter(allocation__student__user=self.request.user).order_by('-date')
