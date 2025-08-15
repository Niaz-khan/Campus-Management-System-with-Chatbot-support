from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum
from .models import (
    Author, Category, Publisher, Book, BookCopy, Borrowing,
    Reservation, Fine, LibraryCard
)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'nationality', 'birth_date', 'death_date', 
        'book_count', 'created_at'
    ]
    list_filter = ['nationality', 'birth_date', 'created_at']
    search_fields = ['name', 'biography', 'nationality']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Books'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'parent', 'book_count', 'color_preview', 'created_at'
    ]
    list_filter = ['parent', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at']
    
    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Books'
    
    def color_preview(self, obj):
        if obj.color:
            return format_html(
                '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 3px;">{}</span>',
                obj.color, obj.color
            )
        return '-'
    color_preview.short_description = 'Color'

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'established_year', 'book_count', 'created_at'
    ]
    list_filter = ['established_year', 'created_at']
    search_fields = ['name', 'address', 'email']
    ordering = ['name']
    readonly_fields = ['created_at']
    
    def book_count(self, obj):
        return obj.book_set.count()
    book_count.short_description = 'Books'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'isbn', 'category', 'book_type', 'total_copies',
        'available_copies', 'status', 'created_at'
    ]
    list_filter = [
        'book_type', 'status', 'category', 'language', 'publication_date'
    ]
    search_fields = [
        'title', 'subtitle', 'isbn', 'isbn13', 'description'
    ]
    ordering = ['title']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    filter_horizontal = ['authors']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'isbn', 'isbn13', 'book_type')
        }),
        ('Classification', {
            'fields': ('category', 'authors', 'publisher')
        }),
        ('Details', {
            'fields': ('publication_date', 'edition', 'pages', 'language', 'description')
        }),
        ('Media', {
            'fields': ('cover_image', 'price')
        }),
        ('Inventory', {
            'fields': ('status', 'total_copies', 'available_copies', 'location', 'tags')
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = [
        'copy_number', 'book_title', 'condition', 'acquisition_date',
        'cost', 'last_maintenance'
    ]
    list_filter = ['condition', 'acquisition_date', 'last_maintenance']
    search_fields = ['copy_number', 'book__title', 'book__isbn']
    ordering = ['copy_number']
    readonly_fields = ['acquisition_date', 'created_at']
    date_hierarchy = 'acquisition_date'
    
    def book_title(self, obj):
        return obj.book.title
    book_title.short_description = 'Book Title'

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = [
        'student_name', 'book_title', 'borrowed_date', 'due_date',
        'status', 'renewed_count', 'fine_amount', 'is_overdue_display'
    ]
    list_filter = [
        'status', 'borrowed_date', 'due_date', 'renewed_count'
    ]
    search_fields = [
        'student__user__first_name', 'student__user__last_name',
        'student__roll_number', 'book_copy__book__title'
    ]
    ordering = ['-borrowed_date']
    readonly_fields = ['borrowed_date', 'fine_amount', 'created_at', 'updated_at']
    date_hierarchy = 'borrowed_date'
    
    def student_name(self, obj):
        return obj.student.user.get_full_name()
    student_name.short_description = 'Student'
    
    def book_title(self, obj):
        return obj.book_copy.book.title
    book_title.short_description = 'Book'
    
    def is_overdue_display(self, obj):
        if obj.is_overdue:
            return format_html(
                '<span style="color: red; font-weight: bold;">{} days overdue</span>',
                obj.days_overdue
            )
        return 'On time'
    is_overdue_display.short_description = 'Overdue Status'
    
    fieldsets = (
        ('Borrowing Information', {
            'fields': ('student', 'book_copy', 'borrowed_date', 'due_date')
        }),
        ('Status', {
            'fields': ('status', 'renewed_count', 'max_renewals')
        }),
        ('Return Information', {
            'fields': ('returned_date', 'returned_to')
        }),
        ('Fines', {
            'fields': ('fine_amount', 'notes')
        }),
        ('System Fields', {
            'fields': ('issued_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'student_name', 'book_title', 'reservation_date', 'expiry_date',
        'status'
    ]
    list_filter = ['status', 'reservation_date', 'expiry_date']
    search_fields = [
        'student__user__first_name', 'student__user__last_name',
        'student__roll_number', 'book__title'
    ]
    ordering = ['-reservation_date']
    readonly_fields = ['reservation_date', 'created_at']
    date_hierarchy = 'reservation_date'
    
    def student_name(self, obj):
        return obj.student.user.get_full_name()
    student_name.short_description = 'Student'
    
    def book_title(self, obj):
        return obj.book.title
    book_title.short_description = 'Book'

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = [
        'student_name', 'book_title', 'fine_type', 'amount',
        'is_paid', 'created_at'
    ]
    list_filter = ['fine_type', 'is_paid', 'created_at']
    search_fields = [
        'borrowing__student__user__first_name',
        'borrowing__student__user__last_name',
        'borrowing__student__roll_number'
    ]
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def student_name(self, obj):
        return obj.borrowing.student.user.get_full_name()
    student_name.short_description = 'Student'
    
    def book_title(self, obj):
        return obj.borrowing.book_copy.book.title
    book_title.short_description = 'Book'

@admin.register(LibraryCard)
class LibraryCardAdmin(admin.ModelAdmin):
    list_display = [
        'card_number', 'student_name', 'issue_date', 'expiry_date',
        'status', 'max_books', 'is_expired_display'
    ]
    list_filter = ['status', 'issue_date', 'expiry_date']
    search_fields = [
        'card_number', 'student__user__first_name',
        'student__user__last_name', 'student__roll_number'
    ]
    ordering = ['-issue_date']
    readonly_fields = ['issue_date', 'created_at', 'updated_at']
    date_hierarchy = 'issue_date'
    
    def student_name(self, obj):
        return obj.student.user.get_full_name()
    student_name.short_description = 'Student'
    
    def is_expired_display(self, obj):
        if obj.is_expired:
            return format_html(
                '<span style="color: red; font-weight: bold;">Expired</span>'
            )
        elif obj.days_until_expiry <= 30:
            return format_html(
                '<span style="color: orange;">Expires in {} days</span>',
                obj.days_until_expiry
            )
        return 'Active'
    is_expired_display.short_description = 'Expiry Status'

# Custom admin actions
@admin.action(description="Mark selected borrowings as overdue")
def mark_overdue(modeladmin, request, queryset):
    from datetime import date
    today = date.today()
    updated = queryset.filter(
        due_date__lt=today, 
        status='active'
    ).update(status='overdue')
    modeladmin.message_user(request, f"{updated} borrowings marked as overdue.")

@admin.action(description="Generate library report")
def generate_library_report(modeladmin, request, queryset):
    # This would generate a detailed library report
    pass

# Add actions to BorrowingAdmin
BorrowingAdmin.actions = [mark_overdue, generate_library_report]
