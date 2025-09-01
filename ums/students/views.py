from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import StudentProfile
from .serializers import StudentProfileSerializer
from users.permissions import IsAdmin, IsFaculty

# Admin and Faculty can list all students
class StudentListView(generics.ListAPIView):
    queryset = StudentProfile.objects.select_related('user', 'batch', 'program').all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAdmin | IsFaculty]

# Retrieve or update a single student profile
class StudentDetailView(generics.RetrieveUpdateAPIView):
    queryset = StudentProfile.objects.select_related('user', 'batch', 'program').all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAdmin | IsFaculty]

# For students to view their own profile
class MyStudentProfileView(generics.RetrieveAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.student_profile
