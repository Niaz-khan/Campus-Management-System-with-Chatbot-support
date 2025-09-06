from django.contrib import admin
from .models import Book, BookBorrow, BookFine

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "total_copies", "available_copies", "created_at")
    search_fields = ("title", "author", "isbn")
    list_filter = ("category",)

@admin.register(BookBorrow)
class BookBorrowAdmin(admin.ModelAdmin):
    list_display = ("student", "book", "borrowed_at", "due_date", "is_returned", "returned_at")
    list_filter = ("is_returned", "due_date")
    search_fields = ("student__roll_no", "book__title", "book__isbn")

@admin.register(BookFine)
class BookFineAdmin(admin.ModelAdmin):
    list_display = ("borrow_record", "fine_amount", "is_paid", "waived", "created_at")
    list_filter = ("is_paid", "waived")
    search_fields = ("borrow_record__student__roll_no", "borrow_record__book__title")
