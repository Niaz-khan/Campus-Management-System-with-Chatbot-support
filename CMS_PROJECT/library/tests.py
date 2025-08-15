from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, time, datetime, timedelta

from .models import (
    Author, Category, Publisher, Book, BookCopy, Borrowing,
    Reservation, Fine, LibraryCard
)

User = get_user_model()

class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name='John Doe',
            biography='A prolific writer',
            nationality='American',
            birth_date=date(1980, 1, 1)
        )

    def test_author_creation(self):
        self.assertEqual(self.author.name, 'John Doe')
        self.assertEqual(self.author.biography, 'A prolific writer')
        self.assertEqual(self.author.nationality, 'American')
        self.assertEqual(str(self.author), 'John Doe')

    def test_author_optional_fields(self):
        author = Author.objects.create(name='Jane Smith')
        self.assertEqual(author.biography, '')
        self.assertIsNone(author.birth_date)

class CategoryModelTest(TestCase):
    def setUp(self):
        self.parent_category = Category.objects.create(
            name='Fiction',
            description='Fictional literature',
            color='#ff0000'
        )
        self.child_category = Category.objects.create(
            name='Science Fiction',
            description='Science fiction books',
            parent=self.parent_category,
            color='#00ff00'
        )

    def test_category_creation(self):
        self.assertEqual(self.parent_category.name, 'Fiction')
        self.assertEqual(self.child_category.parent, self.parent_category)
        self.assertEqual(str(self.parent_category), 'Fiction')

    def test_category_hierarchy(self):
        self.assertEqual(self.parent_category.children.count(), 1)
        self.assertEqual(self.child_category.parent.name, 'Fiction')

class PublisherModelTest(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(
            name='Test Publisher',
            address='123 Test Street',
            email='test@publisher.com',
            established_year=1990
        )

    def test_publisher_creation(self):
        self.assertEqual(self.publisher.name, 'Test Publisher')
        self.assertEqual(self.publisher.established_year, 1990)
        self.assertEqual(str(self.publisher), 'Test Publisher')

class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.category = Category.objects.create(name='Test Category')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890',
            book_type='textbook',
            category=self.category,
            publisher=self.publisher,
            total_copies=5,
            available_copies=5
        )
        self.book.authors.add(self.author)

    def test_book_creation(self):
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.isbn, '1234567890')
        self.assertEqual(self.book.book_type, 'textbook')
        self.assertEqual(self.book.total_copies, 5)
        self.assertEqual(self.book.available_copies, 5)
        self.assertEqual(str(self.book), 'Test Book')

    def test_book_authors_relationship(self):
        self.assertEqual(self.book.authors.count(), 1)
        self.assertEqual(self.book.authors.first(), self.author)

    def test_book_copy_management(self):
        # Test auto-update of available copies
        self.book.total_copies = 10
        self.book.save()
        self.assertEqual(self.book.available_copies, 10)

class BookCopyModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.category = Category.objects.create(name='Test Category')
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890',
            book_type='textbook',
            category=self.category,
            total_copies=1,
            available_copies=1
        )
        self.book.authors.add(self.author)
        
        self.book_copy = BookCopy.objects.create(
            book=self.book,
            copy_number='COPY001',
            condition='available'
        )

    def test_book_copy_creation(self):
        self.assertEqual(self.book_copy.copy_number, 'COPY001')
        self.assertEqual(self.book_copy.condition, 'available')
        self.assertEqual(str(self.book_copy), 'Test Book - Copy COPY001')

class BorrowingModelTest(TestCase):
    def setUp(self):
        # Create necessary related objects
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.author = Author.objects.create(name='Test Author')
        self.category = Category.objects.create(name='Test Category')
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890',
            book_type='textbook',
            category=self.category,
            total_copies=1,
            available_copies=1
        )
        self.book.authors.add(self.author)
        
        self.book_copy = BookCopy.objects.create(
            book=self.book,
            copy_number='COPY001',
            condition='available'
        )
        
        # Create a student (assuming Student model exists)
        from students.models import Student
        self.student = Student.objects.create(
            user=self.user,
            roll_number='ST001'
        )
        
        self.borrowing = Borrowing.objects.create(
            student=self.student,
            book_copy=self.book_copy,
            due_date=date.today() + timedelta(days=14),
            issued_by=self.user
        )

    def test_borrowing_creation(self):
        self.assertEqual(self.borrowing.student, self.student)
        self.assertEqual(self.borrowing.book_copy, self.book_copy)
        self.assertEqual(self.borrowing.status, 'active')
        self.assertEqual(str(self.borrowing), f"{self.student} - Test Book")

    def test_borrowing_overdue_property(self):
        # Test not overdue
        self.assertFalse(self.borrowing.is_overdue)
        self.assertEqual(self.borrowing.days_overdue, 0)
        
        # Test overdue
        self.borrowing.due_date = date.today() - timedelta(days=5)
        self.borrowing.save()
        self.assertTrue(self.borrowing.is_overdue)
        self.assertEqual(self.borrowing.days_overdue, 5)

    def test_borrowing_auto_due_date(self):
        borrowing = Borrowing.objects.create(
            student=self.student,
            book_copy=self.book_copy,
            issued_by=self.user
        )
        expected_due_date = date.today() + timedelta(days=14)
        self.assertEqual(borrowing.due_date, expected_due_date)

class ReservationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.author = Author.objects.create(name='Test Author')
        self.category = Category.objects.create(name='Test Category')
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890',
            book_type='textbook',
            category=self.category,
            total_copies=0,
            available_copies=0
        )
        self.book.authors.add(self.author)
        
        from students.models import Student
        self.student = Student.objects.create(
            user=self.user,
            roll_number='ST001'
        )
        
        self.reservation = Reservation.objects.create(
            student=self.student,
            book=self.book
        )

    def test_reservation_creation(self):
        self.assertEqual(self.reservation.student, self.student)
        self.assertEqual(self.reservation.book, self.book)
        self.assertEqual(self.reservation.status, 'pending')
        self.assertEqual(str(self.reservation), f"{self.student} - Test Book")

    def test_reservation_auto_expiry(self):
        # Test that expiry date is set automatically
        expected_expiry = datetime.now() + timedelta(hours=24)
        # Allow for small time differences
        self.assertLess(
            abs((self.reservation.expiry_date - expected_expiry).total_seconds()),
            60  # 1 minute tolerance
        )

class FineModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.author = Author.objects.create(name='Test Author')
        self.category = Category.objects.create(name='Test Category')
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890',
            book_type='textbook',
            category=self.category,
            total_copies=1,
            available_copies=1
        )
        self.book.authors.add(self.author)
        
        self.book_copy = BookCopy.objects.create(
            book=self.book,
            copy_number='COPY001',
            condition='available'
        )
        
        from students.models import Student
        self.student = Student.objects.create(
            user=self.user,
            roll_number='ST001'
        )
        
        self.borrowing = Borrowing.objects.create(
            student=self.student,
            book_copy=self.book_copy,
            due_date=date.today() + timedelta(days=14),
            issued_by=self.user
        )
        
        self.fine = Fine.objects.create(
            borrowing=self.borrowing,
            fine_type='overdue',
            amount=Decimal('5.00'),
            reason='Book returned late',
            created_by=self.user
        )

    def test_fine_creation(self):
        self.assertEqual(self.fine.borrowing, self.borrowing)
        self.assertEqual(self.fine.fine_type, 'overdue')
        self.assertEqual(self.fine.amount, Decimal('5.00'))
        self.assertFalse(self.fine.is_paid)
        self.assertEqual(str(self.fine), f"Fine {self.fine.id} - {self.student} - 5.00")

class LibraryCardModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        from students.models import Student
        self.student = Student.objects.create(
            user=self.user,
            roll_number='ST001'
        )
        
        self.library_card = LibraryCard.objects.create(
            student=self.student,
            card_number='CARD001',
            max_books=5,
            max_days=14,
            issued_by=self.user
        )

    def test_library_card_creation(self):
        self.assertEqual(self.library_card.student, self.student)
        self.assertEqual(self.library_card.card_number, 'CARD001')
        self.assertEqual(self.library_card.status, 'active')
        self.assertEqual(self.library_card.max_books, 5)
        self.assertEqual(str(self.library_card), 'Card CARD001 - Test User')

    def test_library_card_auto_expiry(self):
        # Test that expiry date is set automatically (1 year from issue)
        expected_expiry = date.today() + timedelta(days=365)
        self.assertEqual(self.library_card.expiry_date, expected_expiry)

    def test_library_card_expiry_properties(self):
        # Test not expired
        self.assertFalse(self.library_card.is_expired)
        self.assertGreater(self.library_card.days_until_expiry, 0)
        
        # Test expired
        self.library_card.expiry_date = date.today() - timedelta(days=5)
        self.library_card.save()
        self.assertTrue(self.library_card.is_expired)
        self.assertEqual(self.library_card.days_until_expiry, -5)

class LibraryModelIntegrationTest(TestCase):
    """Integration tests for library operations"""
    
    def setUp(self):
        # Create comprehensive test data
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.author = Author.objects.create(name='Test Author')
        self.category = Category.objects.create(name='Test Category')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890',
            book_type='textbook',
            category=self.category,
            publisher=self.publisher,
            total_copies=3,
            available_copies=3
        )
        self.book.authors.add(self.author)
        
        # Create multiple copies
        self.copy1 = BookCopy.objects.create(
            book=self.book,
            copy_number='COPY001',
            condition='available'
        )
        self.copy2 = BookCopy.objects.create(
            book=self.book,
            copy_number='COPY002',
            condition='available'
        )
        
        from students.models import Student
        self.student = Student.objects.create(
            user=self.user,
            roll_number='ST001'
        )
        
        self.library_card = LibraryCard.objects.create(
            student=self.student,
            card_number='CARD001',
            max_books=5,
            max_days=14,
            issued_by=self.user
        )

    def test_complete_borrowing_cycle(self):
        """Test the complete book borrowing and return cycle"""
        # 1. Borrow a book
        borrowing = Borrowing.objects.create(
            student=self.student,
            book_copy=self.copy1,
            issued_by=self.user
        )
        
        # Check that book copy status changed
        self.copy1.refresh_from_db()
        self.assertEqual(self.copy1.condition, 'borrowed')
        
        # Check that book available copies decreased
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 2)
        
        # 2. Return the book
        borrowing.status = 'returned'
        borrowing.returned_date = date.today()
        borrowing.returned_to = self.user
        borrowing.save()
        
        # Check that book copy status changed back
        self.copy1.refresh_from_db()
        self.assertEqual(self.copy1.condition, 'available')
        
        # Check that book available copies increased
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 3)

    def test_overdue_fine_calculation(self):
        """Test automatic fine calculation for overdue books"""
        # Create an overdue borrowing
        borrowing = Borrowing.objects.create(
            student=self.student,
            book_copy=self.copy1,
            due_date=date.today() - timedelta(days=5),
            issued_by=self.user
        )
        
        # Return the overdue book
        borrowing.status = 'returned'
        borrowing.returned_date = date.today()
        borrowing.returned_to = self.user
        borrowing.save()
        
        # Check that fine was calculated
        self.assertEqual(borrowing.fine_amount, Decimal('5.00'))  # 5 days * $1.00

    def test_book_reservation_system(self):
        """Test book reservation functionality"""
        # Reserve a book
        reservation = Reservation.objects.create(
            student=self.student,
            book=self.book
        )
        
        self.assertEqual(reservation.status, 'pending')
        self.assertIsNotNone(reservation.expiry_date)
        
        # Test unique constraint
        with self.assertRaises(Exception):
            Reservation.objects.create(
                student=self.student,
                book=self.book,
                status='pending'
            )
