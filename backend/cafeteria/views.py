from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from .models import MealPlan, MessSubscription, MealAttendance
from .serializers import MealPlanSerializer, MessSubscriptionSerializer, MealAttendanceSerializer
from notifications.utils import send_notification

class IsAdminOrFaculty(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ('ADMIN','FACULTY'))

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'STUDENT')


# Faculty/Admin APIs
class MealPlanListCreateView(generics.ListCreateAPIView):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer
    permission_classes = [IsAdminOrFaculty]


class MealPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer
    permission_classes = [IsAdminOrFaculty]


class AssignMessSubscriptionView(generics.CreateAPIView):
    queryset = MessSubscription.objects.all()
    serializer_class = MessSubscriptionSerializer
    permission_classes = [IsAdminOrFaculty]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save(subscribed_by=request.user)

        send_notification(
            user=subscription.student.user,
            title="Mess Subscription Assigned",
            message=f"You have been assigned to {subscription.meal_plan.name} from {subscription.start_date}.",
            notification_type="INFO",
            related_object=subscription
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MarkMealAttendanceView(generics.CreateAPIView):
    queryset = MealAttendance.objects.all()
    serializer_class = MealAttendanceSerializer
    permission_classes = [IsAdminOrFaculty]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attendance = serializer.save(marked_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Student APIs
class StudentMySubscriptionsView(generics.ListAPIView):
    serializer_class = MessSubscriptionSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return MessSubscription.objects.filter(student__user=self.request.user, is_active=True)


class StudentMyMealAttendanceView(generics.ListAPIView):
    serializer_class = MealAttendanceSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return MealAttendance.objects.filter(subscription__student__user=self.request.user)
