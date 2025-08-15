from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorViewSet, CategoryViewSet, PublisherViewSet, BookViewSet,
    BookCopyViewSet, BorrowingViewSet, ReservationViewSet,
    FineViewSet, LibraryCardViewSet, LibraryAnalyticsViewSet
)

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'books', BookViewSet)
router.register(r'book-copies', BookCopyViewSet)
router.register(r'borrowings', BorrowingViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'fines', FineViewSet)
router.register(r'library-cards', LibraryCardViewSet)
router.register(r'analytics', LibraryAnalyticsViewSet, basename='library-analytics')

urlpatterns = [
    path('', include(router.urls)),
]
