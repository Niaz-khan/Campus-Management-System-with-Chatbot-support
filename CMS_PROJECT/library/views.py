from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from .models import (
    Author, Category, Publisher, Book, BookCopy, Borrowing,
    Reservation, Fine, LibraryCard
)
from .serializers import (
    AuthorSerializer, CategorySerializer, PublisherSerializer, BookSerializer,
    BookCopySerializer, BorrowingSerializer, ReservationSerializer,
    FineSerializer, LibraryCardSerializer, BookSearchSerializer,
    BorrowingSummarySerializer, LibraryAnalyticsSerializer
)

class AuthorViewSet(viewsets.ModelViewSet):
    """API endpoint for author management"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'biography', 'nationality']
    ordering_fields = ['name', 'birth_date', 'created_at']

    @action(detail=False, methods=['get'])
    def popular_authors(self, request):
        """Get most popular authors based on book count"""
        popular_authors = self.queryset.annotate(
            book_count=Count('books')
        ).filter(book_count__gt=0).order_by('-book_count')[:10]
        
        serializer = self.get_serializer(popular_authors, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint for category management"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    @action(detail=False, methods=['get'])
    def tree_structure(self, request):
        """Get hierarchical category structure"""
        root_categories = self.queryset.filter(parent__isnull=True)
        
        def build_tree(category):
            children = self.queryset.filter(parent=category)
            return {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'color': category.color,
                'icon': category.icon,
                'children': [build_tree(child) for child in children]
            }
        
        tree = [build_tree(cat) for cat in root_categories]
        return Response(tree)

class PublisherViewSet(viewsets.ModelViewSet):
    """API endpoint for publisher management"""
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address', 'email']
    ordering_fields = ['name', 'established_year', 'created_at']

class BookViewSet(viewsets.ModelViewSet):
    """API endpoint for book management"""
    queryset = Book.objects.select_related('category', 'publisher').prefetch_related('authors').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'title', 'subtitle', 'isbn', 'isbn13', 'description',
        'authors__name', 'category__name', 'publisher__name'
    ]
    ordering_fields = ['title', 'publication_date', 'created_at', 'total_copies']

    @action(detail=False, methods=['get'])
    def search_books(self, request):
        """Advanced book search functionality"""
        query = request.query_params.get('query', '')
        category_id = request.query_params.get('category')
        book_type = request.query_params.get('book_type')
        language = request.query_params.get('language')
        available_only = request.query_params.get('available_only', 'false').lower() == 'true'
        
        queryset = self.queryset
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(subtitle__icontains=query) |
                Q(isbn__icontains=query) |
                Q(authors__name__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        if book_type:
            queryset = queryset.filter(book_type=book_type)
        
        if language:
            queryset = queryset.filter(language__iexact=language)
        
        if available_only:
            queryset = queryset.filter(available_copies__gt=0)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available_books(self, request):
        """Get all available books"""
        available_books = self.queryset.filter(available_copies__gt=0)
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular_books(self, request):
        """Get most popular books based on borrowing count"""
        popular_books = self.queryset.annotate(
            borrowing_count=Count('copies__borrowings')
        ).filter(borrowing_count__gt=0).order_by('-borrowing_count')[:20]
        
        serializer = self.get_serializer(popular_books, many=True)
        return Response(serializer.data)

class BookCopyViewSet(viewsets.ModelViewSet):
    """API endpoint for book copy management"""
    queryset = BookCopy.objects.select_related('book').all()
    serializer_class = BookCopySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['copy_number', 'book__title', 'book__isbn']
    ordering_fields = ['copy_number', 'acquisition_date', 'created_at']

    @action(detail=False, methods=['get'])
    def available_copies(self, request):
        """Get all available book copies"""
        available_copies = self.queryset.filter(condition='available')
        serializer = self.get_serializer(available_copies, many=True)
        return Response(serializer.data)

class BorrowingViewSet(viewsets.ModelViewSet):
    """API endpoint for borrowing management"""
    queryset = Borrowing.objects.select_related(
        'student__user', 'book_copy__book', 'issued_by', 'returned_to'
    ).all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'student__user__first_name', 'student__user__last_name',
        'student__roll_number', 'book_copy__book__title'
    ]
    ordering_fields = ['borrowed_date', 'due_date', 'returned_date', 'created_at']

    @action(detail=False, methods=['get'])
    def active_borrowings(self, request):
        """Get all active borrowings"""
        active_borrowings = self.queryset.filter(status='active')
        serializer = self.get_serializer(active_borrowings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def overdue_borrowings(self, request):
        """Get all overdue borrowings"""
        overdue_borrowings = self.queryset.filter(
            status='active',
            due_date__lt=date.today()
        )
        serializer = self.get_serializer(overdue_borrowings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def student_borrowings(self, request):
        """Get borrowings for a specific student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        student_borrowings = self.queryset.filter(student_id=student_id)
        serializer = self.get_serializer(student_borrowings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def renew_book(self, request, pk=None):
        """Renew a borrowed book"""
        borrowing = self.get_object()
        
        if borrowing.status != 'active':
            return Response(
                {'error': 'Book is not currently borrowed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if borrowing.renewed_count >= borrowing.max_renewals:
            return Response(
                {'error': 'Maximum renewals reached'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extend due date by 14 days
        borrowing.due_date += timedelta(days=14)
        borrowing.renewed_count += 1
        borrowing.save()
        
        serializer = self.get_serializer(borrowing)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """Return a borrowed book"""
        borrowing = self.get_object()
        
        if borrowing.status != 'active':
            return Response(
                {'error': 'Book is not currently borrowed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        borrowing.status = 'returned'
        borrowing.returned_date = date.today()
        borrowing.returned_to = request.user
        
        # Calculate fines if overdue
        if borrowing.is_overdue:
            days_overdue = borrowing.days_overdue
            fine_per_day = Decimal('1.00')  # $1 per day
            borrowing.fine_amount = days_overdue * fine_per_day
        
        borrowing.save()
        
        serializer = self.get_serializer(borrowing)
        return Response(serializer.data)

class ReservationViewSet(viewsets.ModelViewSet):
    """API endpoint for reservation management"""
    queryset = Reservation.objects.select_related('student__user', 'book').all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'student__user__first_name', 'student__user__last_name',
        'student__roll_number', 'book__title'
    ]
    ordering_fields = ['reservation_date', 'expiry_date', 'created_at']

    @action(detail=False, methods=['get'])
    def pending_reservations(self, request):
        """Get all pending reservations"""
        pending_reservations = self.queryset.filter(status='pending')
        serializer = self.get_serializer(pending_reservations, many=True)
        return Response(serializer.data)

class FineViewSet(viewsets.ModelViewSet):
    """API endpoint for fine management"""
    queryset = Fine.objects.select_related(
        'borrowing__student__user', 'borrowing__book_copy__book', 'created_by'
    ).all()
    serializer_class = FineSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'borrowing__student__user__first_name', 'borrowing__student__user__last_name',
        'borrowing__student__roll_number'
    ]
    ordering_fields = ['amount', 'created_at', 'paid_date']

    @action(detail=False, methods=['get'])
    def unpaid_fines(self, request):
        """Get all unpaid fines"""
        unpaid_fines = self.queryset.filter(is_paid=False)
        serializer = self.get_serializer(unpaid_fines, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Mark a fine as paid"""
        fine = self.get_object()
        
        if fine.is_paid:
            return Response(
                {'error': 'Fine is already paid'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        fine.is_paid = True
        fine.paid_date = date.today()
        fine.payment_method = request.data.get('payment_method', 'cash')
        fine.save()
        
        serializer = self.get_serializer(fine)
        return Response(serializer.data)

class LibraryCardViewSet(viewsets.ModelViewSet):
    """API endpoint for library card management"""
    queryset = LibraryCard.objects.select_related('student__user', 'issued_by').all()
    serializer_class = LibraryCardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'card_number', 'student__user__first_name', 'student__user__last_name',
        'student__roll_number'
    ]
    ordering_fields = ['issue_date', 'expiry_date', 'created_at']

    @action(detail=False, methods=['get'])
    def active_cards(self, request):
        """Get all active library cards"""
        active_cards = self.queryset.filter(status='active')
        serializer = self.get_serializer(active_cards, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def expired_cards(self, request):
        """Get all expired library cards"""
        expired_cards = self.queryset.filter(
            status='active',
            expiry_date__lt=date.today()
        )
        serializer = self.get_serializer(expired_cards, many=True)
        return Response(serializer.data)

class LibraryAnalyticsViewSet(viewsets.ViewSet):
    """API endpoint for library analytics and reporting"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get comprehensive library dashboard statistics"""
        total_books = Book.objects.count()
        total_copies = BookCopy.objects.count()
        available_copies = BookCopy.objects.filter(condition='available').count()
        borrowed_copies = BookCopy.objects.filter(condition='borrowed').count()
        
        total_students = LibraryCard.objects.filter(status='active').count()
        active_borrowings = Borrowing.objects.filter(status='active').count()
        overdue_borrowings = Borrowing.objects.filter(
            status='active',
            due_date__lt=date.today()
        ).count()
        
        total_fines = Fine.objects.aggregate(total=Sum('amount'))['total'] or 0
        unpaid_fines = Fine.objects.filter(is_paid=False).aggregate(total=Sum('amount'))['total'] or 0
        
        # Popular categories
        popular_categories = Category.objects.annotate(
            book_count=Count('books')
        ).filter(book_count__gt=0).order_by('-book_count')[:5]
        
        # Popular books
        popular_books = Book.objects.annotate(
            borrowing_count=Count('copies__borrowings')
        ).filter(borrowing_count__gt=0).order_by('-borrowing_count')[:10]
        
        analytics_data = {
            'total_books': total_books,
            'total_copies': total_copies,
            'available_copies': available_copies,
            'borrowed_copies': borrowed_copies,
            'total_students': total_students,
            'active_borrowings': active_borrowings,
            'overdue_borrowings': overdue_borrowings,
            'total_fines': total_fines,
            'unpaid_fines': unpaid_fines,
            'popular_categories': [
                {'name': cat.name, 'count': cat.book_count} 
                for cat in popular_categories
            ],
            'popular_books': [
                {'title': book.title, 'count': book.borrowing_count} 
                for book in popular_books
            ]
        }
        
        serializer = LibraryAnalyticsSerializer(analytics_data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def borrowing_summary(self, request):
        """Get borrowing summary for a specific student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        borrowings = Borrowing.objects.filter(student_id=student_id)
        total_borrowed = borrowings.count()
        currently_borrowed = borrowings.filter(status='active').count()
        overdue_books = borrowings.filter(
            status='active',
            due_date__lt=date.today()
        ).count()
        
        total_fines = borrowings.aggregate(total=Sum('fine_amount'))['total'] or 0
        unpaid_fines = Fine.objects.filter(
            borrowing__student_id=student_id,
            is_paid=False
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        summary_data = {
            'student_id': student_id,
            'student_name': borrowings.first().student.user.get_full_name() if borrowings.exists() else '',
            'total_borrowed': total_borrowed,
            'currently_borrowed': currently_borrowed,
            'overdue_books': overdue_books,
            'total_fines': total_fines,
            'unpaid_fines': unpaid_fines,
        }
        
        serializer = BorrowingSummarySerializer(summary_data)
        return Response(serializer.data)
