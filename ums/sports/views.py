from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from .models import Facility, GymMembership, Equipment, EquipmentIssue, Tournament, TournamentRegistration
from .serializers import (
    FacilitySerializer, GymMembershipSerializer, EquipmentSerializer,
    EquipmentIssueSerializer, TournamentSerializer, TournamentRegistrationSerializer
)
from .permissions import IsAdminOrFaculty, IsStudent
from notifications.utils import send_notification
from decimal import Decimal
from django.conf import settings

# Optional fees helper (if you have fees.utils.create_invoice, use it)
# from fees.utils import create_invoice_for_student

# -------- Faculty/Admin APIs --------

# Facilities
class FacilityListCreateView(generics.ListCreateAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [IsAdminOrFaculty]

class FacilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [IsAdminOrFaculty]

# Gym memberships: create and list
class GymMembershipListCreateView(generics.ListCreateAPIView):
    queryset = GymMembership.objects.select_related('student','facility').all()
    serializer_class = GymMembershipSerializer
    permission_classes = [IsAdminOrFaculty]

    def perform_create(self, serializer):
        # optional: create fee invoice here
        membership = serializer.save(issued_by=self.request.user)
        try:
            # create_invoice_for_student(membership.student, membership.price, f"Gym membership {membership.membership_type}")
            pass
        except Exception:
            pass

# Equipment CRUD & issue/return
class EquipmentListCreateView(generics.ListCreateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAdminOrFaculty]

class EquipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAdminOrFaculty]

class IssueEquipmentView(generics.CreateAPIView):
    queryset = EquipmentIssue.objects.all()
    serializer_class = EquipmentIssueSerializer
    permission_classes = [IsAdminOrFaculty]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        equipment = Equipment.objects.select_for_update().filter(id=data.get('equipment'), is_active=True).first()
        if not equipment:
            return Response({"detail":"Equipment not found"}, status=status.HTTP_404_NOT_FOUND)

        qty = int(data.get('quantity',1))
        if not equipment.can_issue(qty):
            return Response({"detail":"Not enough available quantity"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        issue = serializer.save(issued_by=request.user)
        equipment.available_quantity = equipment.available_quantity - qty
        equipment.save(update_fields=['available_quantity'])

        send_notification(
            user=issue.issued_to.user,
            title="Equipment Issued",
            message=f"{qty} x {equipment.name} issued. Due: {issue.due_date}",
            notification_type="INFO",
            related_object=issue
        )
        return Response(self.get_serializer(issue).data, status=status.HTTP_201_CREATED)


class ReturnEquipmentView(generics.UpdateAPIView):
    queryset = EquipmentIssue.objects.all()
    serializer_class = EquipmentIssueSerializer
    permission_classes = [IsAdminOrFaculty]

    def update(self, request, *args, **kwargs):
        issue = self.get_object()
        if issue.returned:
            return Response({"detail":"Already returned"}, status=status.HTTP_400_BAD_REQUEST)

        issue.returned = True
        issue.returned_at = timezone.now().date()

        # calculate overdue fine if any (policy: fixed per day)
        today = timezone.now().date()
        overdue_days = (today - issue.due_date).days if today > issue.due_date else 0
        fine_per_day = Decimal(getattr(settings,'EQUIPMENT_FINE_PER_DAY', '5.00'))
        issue.overdue_fine = (Decimal(overdue_days) * fine_per_day).quantize(Decimal('0.01'))
        issue.save(update_fields=['returned','returned_at','overdue_fine'])

        # restore equipment quantity
        equipment = issue.equipment
        equipment.available_quantity = equipment.available_quantity + issue.quantity
        equipment.save(update_fields=['available_quantity'])

        if issue.overdue_fine > 0:
            send_notification(
                user=issue.issued_to.user,
                title="Equipment Overdue Fine",
                message=f"A fine of {issue.overdue_fine} applied for late return of {equipment.name}.",
                notification_type="ALERT",
                related_object=issue
            )

        return Response(self.get_serializer(issue).data, status=status.HTTP_200_OK)


# Tournaments & registrations
class TournamentListCreateView(generics.ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAdminOrFaculty]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TournamentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAdminOrFaculty]

class TournamentRegistrationListView(generics.ListAPIView):
    queryset = TournamentRegistration.objects.select_related('student','tournament').all()
    serializer_class = TournamentRegistrationSerializer
    permission_classes = [IsAdminOrFaculty]

# -------- Student APIs --------

class StudentMyMembershipView(generics.ListAPIView):
    serializer_class = GymMembershipSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return GymMembership.objects.filter(student__user=self.request.user).order_by('-start_date')

class StudentAvailableFacilitiesView(generics.ListAPIView):
    serializer_class = FacilitySerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Facility.objects.filter(is_active=True)

class StudentIssueListView(generics.ListAPIView):
    serializer_class = EquipmentIssueSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return EquipmentIssue.objects.filter(issued_to__user=self.request.user).order_by('-issue_date')

class StudentAvailableTournamentsView(generics.ListAPIView):
    serializer_class = TournamentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        today = timezone.now().date()
        return Tournament.objects.filter(is_active=True, start_date__gte=today)

class StudentRegisterTournamentView(generics.CreateAPIView):
    queryset = TournamentRegistration.objects.all()
    serializer_class = TournamentRegistrationSerializer
    permission_classes = [IsStudent]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['student'] = request.user.studentprofile.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        tournament = Tournament.objects.get(id=data['tournament'])
        if tournament.registrations_count >= tournament.capacity:
            return Response({"detail":"Tournament capacity full."}, status=status.HTTP_400_BAD_REQUEST)

        registration = serializer.save()
        send_notification(
            user=registration.student.user,
            title="Tournament Registration",
            message=f"You are registered for {tournament.name}.",
            notification_type="INFO",
            related_object=registration
        )
        return Response(self.get_serializer(registration).data, status=status.HTTP_201_CREATED)
