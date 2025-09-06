from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from .models import Book, BookBorrow, BookFine
from .serializers import BookSerializer, BookBorrowSerializer, BookFineSerializer
from .permissions import IsFacultyOrAdmin
from notifications.utils import send_notification

# Books CRUD
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsFacultyOrAdmin]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsFacultyOrAdmin]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsFacultyOrAdmin]


# Issue (borrow) book
class BookBorrowCreateView(generics.CreateAPIView):
    queryset = BookBorrow.objects.all()
    serializer_class = BookBorrowSerializer
    permission_classes = [IsFacultyOrAdmin]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        book_id = data.get('book')
        student_id = data.get('student')
        due_date = data.get('due_date')

        book = Book.objects.select_for_update().filter(id=book_id).first()
        if not book:
            return Response({"detail":"Book not found"}, status=status.HTTP_404_NOT_FOUND)
        if not book.can_borrow():
            return Response({"detail":"No available copies"}, status=status.HTTP_400_BAD_REQUEST)

        # create borrow record
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        borrow = serializer.save()
        # decrement available copies
        book.available_copies = book.available_copies - 1
        book.save(update_fields=['available_copies'])

        # notify student
        send_notification(
            user=borrow.student.user,
            title="Book Issued",
            message=f"Book '{book.title}' has been issued to you. Due date: {borrow.due_date}",
            notification_type="INFO",
            related_object=borrow
        )

        return Response(self.get_serializer(borrow).data, status=status.HTTP_201_CREATED)


# Return book
class BookReturnView(generics.UpdateAPIView):
    queryset = BookBorrow.objects.all()
    serializer_class = BookBorrowSerializer
    permission_classes = [IsFacultyOrAdmin]

    def update(self, request, *args, **kwargs):
        borrow = self.get_object()
        if borrow.is_returned:
            return Response({"detail":"Already returned"}, status=status.HTTP_400_BAD_REQUEST)

        borrow.is_returned = True
        borrow.returned_at = timezone.now().date()
        borrow.save(update_fields=['is_returned', 'returned_at'])

        # update available copies
        book = borrow.book
        book.available_copies = book.available_copies + 1
        book.save(update_fields=['available_copies'])

        # if fine exists and not paid, notify student
        fine = getattr(borrow, 'fine', None)
        if fine and fine.fine_amount > 0 and not fine.is_paid and not fine.waived:
            send_notification(
                user=borrow.student.user,
                title="Library Fine Due",
                message=f"Fine of {fine.fine_amount} is due for returned book '{book.title}'.",
                notification_type="ALERT",
                related_object=fine
            )

        return Response({"detail":"Book returned and inventory updated."}, status=status.HTTP_200_OK)


# Manage fines (Admin can update/waive)
class FineListView(generics.ListAPIView):
    queryset = BookFine.objects.all()
    serializer_class = BookFineSerializer
    permission_classes = [IsFacultyOrAdmin]


class FineDetailView(generics.RetrieveUpdateAPIView):
    queryset = BookFine.objects.all()
    serializer_class = BookFineSerializer
    permission_classes = [IsFacultyOrAdmin]


class StudentAvailableBooksView(generics.ListAPIView):
    queryset = Book.objects.filter(available_copies__gt=0)
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentBorrowedBooksView(generics.ListAPIView):
    serializer_class = BookBorrowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BookBorrow.objects.filter(student__user=self.request.user).order_by('-borrowed_at')


class StudentFinesView(generics.ListAPIView):
    serializer_class = BookFineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BookFine.objects.filter(borrow_record__student__user=self.request.user, is_paid=False, waived=False)

