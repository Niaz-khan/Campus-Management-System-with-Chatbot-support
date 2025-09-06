from rest_framework import serializers
from .models import MealPlan, MessSubscription, MealAttendance
from students.serializers import StudentProfileSerializer

class MealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = ['id', 'name', 'meal_type', 'menu', 'price_per_day', 'is_active', 'created_at']


class MessSubscriptionSerializer(serializers.ModelSerializer):
    student_details = StudentProfileSerializer(source='student', read_only=True)
    meal_plan_name = serializers.CharField(source='meal_plan.name', read_only=True)

    class Meta:
        model = MessSubscription
        fields = [
            'id', 'student', 'student_details',
            'meal_plan', 'meal_plan_name',
            'start_date', 'end_date', 'monthly_fee',
            'is_active', 'subscribed_by', 'created_at'
        ]
        read_only_fields = ['subscribed_by', 'created_at']


class MealAttendanceSerializer(serializers.ModelSerializer):
    student_roll_no = serializers.CharField(source='subscription.student.roll_no', read_only=True)
    meal_plan_name = serializers.CharField(source='subscription.meal_plan.name', read_only=True)

    class Meta:
        model = MealAttendance
        fields = [
            'id', 'subscription', 'student_roll_no', 'meal_plan_name',
            'date', 'attended', 'remarks', 'created_at'
        ]
