from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import User
from .serializers import UserRegisterSerializer, UserDetailSerializer, CustomTokenObtainPairSerializer

# 1. User Registration View
# -------------------------
# Allows anyone (no authentication required) to create a new user account.
# By default, users will be created as STUDENT unless a higher role is set by admin.
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can register (can later restrict to admin-only)

    def create(self, request, *args, **kwargs):
        # Handle the POST request to create a user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "User registered successfully.",
            "user": UserDetailSerializer(user).data
        }, status=status.HTTP_201_CREATED)


# 2. JWT Login View
# -----------------
# Handles login and returns access & refresh tokens.
# Uses SimpleJWT's TokenObtainPairView with a custom serializer for better response format.
class UserLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# 3. JWT Token Refresh View
# -------------------------
# Used to refresh access token using the refresh token.
class UserTokenRefreshView(TokenRefreshView):
    pass


# 4. Current User Profile View
# ----------------------------
# Returns details of the logged-in user.
# Useful for frontend to fetch role & basic profile info after login.
class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Always return the current logged-in user
        return self.request.user
