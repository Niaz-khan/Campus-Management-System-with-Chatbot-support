from rest_framework import serializers
from .models import (
    Author, Category, Publisher, Book, BookCopy, Borrowing, 
    Reservation, Fine, LibraryCard
)

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id', 'name', 'biography', 'birth_date', 'death_date',
            'nationality', 'website', 'photo', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class CategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'parent', 'parent_name',
            'color', 'icon', 'children_count', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_children_count(self, obj):
        return obj.children.count()

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = [
            'id', 'name', 'address', 'phone', 'email', 'website',
            'established_year', 'created_at'
        ]
        read_only_fields = ['created_at']

class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    publisher_name = serializers.CharField(source='publisher.name', read_only=True)
    authors_names = serializers.SerializerMethodField()
    book_type_display = serializers.CharField(source='get_book_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'subtitle', 'isbn', 'isbn13', 'book_type',
            'book_type_display', 'category', 'category_name', 'authors',
            'authors_names', 'publisher', 'publisher_name', 'publication_date',
            'edition', 'pages', 'language', 'description', 'cover_image',
            'price', 'status', 'status_display', 'total_copies',
            'available_copies', 'location', 'tags', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_authors_names(self, obj):
        return [author.name for author in obj.authors.all()]

class BookCopySerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_isbn = serializers.CharField(source='book.isbn', read_only=True)
    condition_display = serializers.CharField(source='get_condition_display', read_only=True)

    class Meta:
        model = BookCopy
        fields = [
            'id', 'book', 'book_title', 'book_isbn', 'copy_number',
            'acquisition_date', 'cost', 'condition', 'condition_display',
            'notes', 'last_maintenance', 'created_at'
        ]
        read_only_fields = ['acquisition_date', 'created_at']

class BorrowingSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    book_title = serializers.CharField(source='book_copy.book.title', read_only=True)
    book_isbn = serializers.CharField(source='book_copy.book.isbn', read_only=True)
    copy_number = serializers.CharField(source='book_copy.copy_number', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    issued_by_name = serializers.CharField(source='issued_by.get_full_name', read_only=True)
    returned_to_name = serializers.CharField(source='returned_to.get_full_name', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    days_overdue = serializers.IntegerField(read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            'id', 'student', 'student_name', 'student_roll', 'book_copy',
            'book_title', 'book_isbn', 'copy_number', 'borrowed_date',
            'due_date', 'returned_date', 'status', 'status_display',
            'renewed_count', 'max_renewals', 'fine_amount', 'notes',
            'issued_by', 'issued_by_name', 'returned_to', 'returned_to_name',
            'is_overdue', 'days_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['borrowed_date', 'fine_amount', 'created_at', 'updated_at']

class ReservationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_isbn = serializers.CharField(source='book.isbn', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'student', 'student_name', 'student_roll', 'book',
            'book_title', 'book_isbn', 'reservation_date', 'expiry_date',
            'status', 'status_display', 'notes', 'created_at'
        ]
        read_only_fields = ['reservation_date', 'created_at']

class FineSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='borrowing.student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='borrowing.student.roll_number', read_only=True)
    book_title = serializers.CharField(source='borrowing.book_copy.book.title', read_only=True)
    fine_type_display = serializers.CharField(source='get_fine_type_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = Fine
        fields = [
            'id', 'borrowing', 'student_name', 'student_roll', 'book_title',
            'fine_type', 'fine_type_display', 'amount', 'reason', 'is_paid',
            'paid_date', 'payment_method', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class LibraryCardSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    issued_by_name = serializers.CharField(source='issued_by.get_full_name', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    days_until_expiry = serializers.IntegerField(read_only=True)

    class Meta:
        model = LibraryCard
        fields = [
            'id', 'student', 'student_name', 'student_roll', 'card_number',
            'issue_date', 'expiry_date', 'status', 'status_display',
            'max_books', 'max_days', 'issued_by', 'issued_by_name',
            'notes', 'is_expired', 'days_until_expiry', 'created_at', 'updated_at'
        ]
        read_only_fields = ['issue_date', 'created_at', 'updated_at']

class BookSearchSerializer(serializers.Serializer):
    """Serializer for book search functionality"""
    query = serializers.CharField(help_text="Search query for title, author, or ISBN")
    category = serializers.IntegerField(required=False, help_text="Category ID")
    book_type = serializers.ChoiceField(choices=Book.BOOK_TYPE_CHOICES, required=False)
    language = serializers.CharField(required=False, help_text="Language filter")
    available_only = serializers.BooleanField(default=False, help_text="Show only available books")

class BorrowingSummarySerializer(serializers.Serializer):
    """Serializer for borrowing summary"""
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    total_borrowed = serializers.IntegerField()
    currently_borrowed = serializers.IntegerField()
    overdue_books = serializers.IntegerField()
    total_fines = serializers.DecimalField(max_digits=10, decimal_places=2)
    unpaid_fines = serializers.DecimalField(max_digits=10, decimal_places=2)

class LibraryAnalyticsSerializer(serializers.Serializer):
    """Serializer for library analytics"""
    total_books = serializers.IntegerField()
    total_copies = serializers.IntegerField()
    available_copies = serializers.IntegerField()
    borrowed_copies = serializers.IntegerField()
    total_students = serializers.IntegerField()
    active_borrowings = serializers.IntegerField()
    overdue_borrowings = serializers.IntegerField()
    total_fines = serializers.DecimalField(max_digits=10, decimal_places=2)
    popular_categories = serializers.ListField()
    popular_books = serializers.ListField()
