from rest_framework import serializers
from .models import Book, BookBorrow, BookFine
from students.serializers import StudentProfileSerializer  # To display borrower info

# 1. Book Serializer
class BookSerializer(serializers.ModelSerializer):
    added_by_name = serializers.CharField(source='added_by.get_full_name', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'category', 'isbn',
            'total_copies', 'available_copies',
            'added_by', 'added_by_name', 'created_at'
        ]
        read_only_fields = ['added_by_name', 'created_at']


# 2. Book Borrow Serializer
class BookBorrowSerializer(serializers.ModelSerializer):
    student_details = StudentProfileSerializer(source='student', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = BookBorrow
        fields = [
            'id', 'student', 'student_details',
            'book', 'book_title',
            'borrowed_at', 'due_date', 'returned_at', 'is_returned'
        ]
        read_only_fields = ['borrowed_at', 'book_title', 'student_details']


# 3. Book Fine Serializer
class BookFineSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='borrow_record.book.title', read_only=True)
    student_roll_no = serializers.CharField(source='borrow_record.student.roll_no', read_only=True)

    class Meta:
        model = BookFine
        fields = [
            'id', 'borrow_record', 'book_title', 'student_roll_no',
            'fine_amount', 'is_paid', 'remarks'
        ]


