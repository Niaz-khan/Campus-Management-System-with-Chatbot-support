from django.urls import path
from . import views

urlpatterns = [
    # Faculty/Admin
    path('faculty/meal-plans/', views.MealPlanListCreateView.as_view(), name='meal-plan-list-create'),
    path('faculty/meal-plans/<int:pk>/', views.MealPlanDetailView.as_view(), name='meal-plan-detail'),
    path('faculty/subscribe/', views.AssignMessSubscriptionView.as_view(), name='assign-mess-subscription'),
    path('faculty/mark-attendance/', views.MarkMealAttendanceView.as_view(), name='mark-meal-attendance'),

    # Student
    path('student/my-subscriptions/', views.StudentMySubscriptionsView.as_view(), name='student-my-subscriptions'),
    path('student/my-attendance/', views.StudentMyMealAttendanceView.as_view(), name='student-my-attendance'),
]
