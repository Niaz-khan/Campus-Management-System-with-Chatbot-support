from django.urls import path
from .views import UserRegisterView, UserLoginView, UserTokenRefreshView, UserProfileView

urlpatterns = [
    # User Registration
    path('register/', UserRegisterView.as_view(), name='user-register'),

    # Login (JWT Token Obtain)
    path('login/', UserLoginView.as_view(), name='user-login'),

    # Refresh Access Token
    path('token/refresh/', UserTokenRefreshView.as_view(), name='token-refresh'),

    # Get Current User Profile
    path('me/', UserProfileView.as_view(), name='user-profile'),
]
