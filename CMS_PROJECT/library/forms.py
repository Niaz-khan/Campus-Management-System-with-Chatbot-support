from django import forms
from .models import (
    Author, Category, Publisher, Book, BookCopy, Borrowing,
    Reservation, Fine, LibraryCard
)

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            'name', 'biography', 'birth_date', 'death_date',
            'nationality', 'website', 'photo'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'biography': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'death_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name', 'description', 'parent', 'color', 'icon'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fas fa-book'}),
        }

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = [
            'name', 'address', 'phone', 'email', 'website', 'established_year'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'established_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'subtitle', 'isbn', 'isbn13', 'book_type',
            'category', 'authors', 'publisher', 'publication_date',
            'edition', 'pages', 'language', 'description', 'cover_image',
            'price', 'status', 'total_copies', 'location', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn13': forms.TextInput(attrs={'class': 'form-control'}),
            'book_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'authors': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'edition': forms.TextInput(attrs={'class': 'form-control'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'total_copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated tags'}),
        }

class BookCopyForm(forms.ModelForm):
    class Meta:
        model = BookCopy
        fields = [
            'book', 'copy_number', 'cost', 'condition', 'notes'
        ]
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'copy_number': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BorrowingForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = [
            'student', 'book_copy', 'due_date', 'max_renewals', 'notes'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'book_copy': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'max_renewals': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'student', 'book', 'notes'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'book': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class FineForm(forms.ModelForm):
    class Meta:
        model = Fine
        fields = [
            'borrowing', 'fine_type', 'amount', 'reason', 'payment_method'
        ]
        widgets = {
            'borrowing': forms.Select(attrs={'class': 'form-control'}),
            'fine_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LibraryCardForm(forms.ModelForm):
    class Meta:
        model = LibraryCard
        fields = [
            'student', 'card_number', 'expiry_date', 'max_books',
            'max_days', 'notes'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'max_books': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BookSearchForm(forms.Form):
    """Form for advanced book search"""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, author, ISBN, or description'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    book_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Book.BOOK_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    language = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Language'})
    )
    available_only = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Min Price'})
    )
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Max Price'})
    )

class BorrowingSearchForm(forms.Form):
    """Form for searching borrowings"""
    student = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + Borrowing.BORROW_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    from_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    to_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    overdue_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import here to avoid circular imports
        from students.models import Student
        self.fields['student'].queryset = Student.objects.all()

class FineSearchForm(forms.Form):
    """Form for searching fines"""
    fine_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Fine.FINE_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_paid = forms.ChoiceField(
        choices=[('', 'All'), ('true', 'Paid'), ('false', 'Unpaid')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_amount = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Min Amount'})
    )
    max_amount = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Max Amount'})
    )
    from_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    to_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
