from django.urls import path
from .views import faculty as faculty_views
from .views import student as student_views

urlpatterns = [
    # Faculty / Admin
    path('faculty/books/', faculty_views.BookListView.as_view(), name='lib-books-list'),
    path('faculty/books/create/', faculty_views.BookCreateView.as_view(), name='lib-book-create'),
    path('faculty/books/<int:pk>/', faculty_views.BookDetailView.as_view(), name='lib-book-detail'),

    path('faculty/borrow/', faculty_views.BookBorrowCreateView.as_view(), name='lib-borrow-create'),
    path('faculty/borrow/<int:pk>/return/', faculty_views.BookReturnView.as_view(), name='lib-borrow-return'),

    path('faculty/fines/', faculty_views.FineListView.as_view(), name='lib-fines-list'),
    path('faculty/fines/<int:pk>/', faculty_views.FineDetailView.as_view(), name='lib-fine-detail'),

    # Student
    path('student/books/', student_views.StudentAvailableBooksView.as_view(), name='lib-student-books'),
    path('student/borrowed/', student_views.StudentBorrowedBooksView.as_view(), name='lib-student-borrowed'),
    path('student/fines/', student_views.StudentFinesView.as_view(), name='lib-student-fines'),
]
