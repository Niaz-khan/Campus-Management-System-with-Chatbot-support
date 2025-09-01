from rest_framework import generics, permissions
from .models import Batch, Program
from .serializers import BatchSerializer, ProgramSerializer
from users.permissions import IsAdmin  # restrict write access to admins

# Batch APIs
class BatchListCreateView(generics.ListCreateAPIView):
    """
    GET: List all batches
    POST: Create a new batch (Admin only)
    """
    queryset = Batch.objects.all().order_by('-start_date')
    serializer_class = BatchSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


class BatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve batch
    PUT/PATCH: Update batch (Admin only)
    DELETE: Delete batch (Admin only)
    """
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


# Program APIs
class ProgramListCreateView(generics.ListCreateAPIView):
    """
    GET: List all programs
    POST: Create a new program (Admin only)
    """
    queryset = Program.objects.select_related('batch').all()
    serializer_class = ProgramSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


class ProgramDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve program
    PUT/PATCH: Update program (Admin only)
    DELETE: Delete program (Admin only)
    """
    queryset = Program.objects.select_related('batch').all()
    serializer_class = ProgramSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]
