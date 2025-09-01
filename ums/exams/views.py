from rest_framework import generics
from .models import Exam
from .serializers import ExamSerializer
from users.permissions import IsAdmin, IsFaculty, IsStudent

# Admin & Faculty: List and create exams
class ExamListCreateView(generics.ListCreateAPIView):
    """
    GET: List all exams (Admin, Faculty, Students)
    POST: Create a new exam (Faculty & Admin)
    """
    queryset = Exam.objects.select_related('course', 'created_by').all()
    serializer_class = ExamSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsFaculty() | IsAdmin()]
        return [IsAdmin() | IsFaculty() | IsStudent()]

# Admin & Faculty: Retrieve, update, delete exam
class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve exam details
    PUT/PATCH: Update exam (Faculty & Admin)
    DELETE: Delete exam (Admin only)
    """
    queryset = Exam.objects.select_related('course', 'created_by').all()
    serializer_class = ExamSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsFaculty() | IsAdmin()]
        if self.request.method == 'DELETE':
            return [IsAdmin()]
        return [IsAdmin() | IsFaculty() | IsStudent()]
