from django.urls import path
from . import views

urlpatterns = [
    # Faculty / Admin
    path('faculty/books/', views.BookListView.as_view(), name='lib-books-list'),
    path('faculty/books/create/', views.BookCreateView.as_view(), name='lib-book-create'),
    path('faculty/books/<int:pk>/', views.BookDetailView.as_view(), name='lib-book-detail'),

    path('faculty/borrow/', views.BookBorrowCreateView.as_view(), name='lib-borrow-create'),
    path('faculty/borrow/<int:pk>/return/', views.BookReturnView.as_view(), name='lib-borrow-return'),

    path('faculty/fines/', views.FineListView.as_view(), name='lib-fines-list'),
    path('faculty/fines/<int:pk>/', views.FineDetailView.as_view(), name='lib-fine-detail'),

    # Student
    path('student/books/', views.StudentAvailableBooksView.as_view(), name='lib-student-books'),
    path('student/borrowed/', views.StudentBorrowedBooksView.as_view(), name='lib-student-borrowed'),
    path('student/fines/', views.StudentFinesView.as_view(), name='lib-student-fines'),
]
