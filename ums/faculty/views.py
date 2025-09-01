from rest_framework import generics, permissions
from .models import FacultyProfile
from .serializers import FacultyProfileSerializer
from users.permissions import IsAdmin, IsFaculty

# Admin: List all faculty
class FacultyListCreateView(generics.ListCreateAPIView):
    """
    GET: List all faculty members
    POST: Add a faculty profile (Admin only)
    """
    queryset = FacultyProfile.objects.select_related('user').all()
    serializer_class = FacultyProfileSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsAdmin()]

# Admin & Faculty: View/update single faculty profile
class FacultyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve faculty profile
    PUT/PATCH: Update profile (Admin only)
    DELETE: Remove faculty (Admin only)
    """
    queryset = FacultyProfile.objects.select_related('user').all()
    serializer_class = FacultyProfileSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdmin()]
        return [IsAdmin() | IsFaculty()]

# Faculty: View their own profile
class MyFacultyProfileView(generics.RetrieveAPIView):
    serializer_class = FacultyProfileSerializer
    permission_classes = [IsFaculty]

    def get_object(self):
        return self.request.user.faculty_profile
