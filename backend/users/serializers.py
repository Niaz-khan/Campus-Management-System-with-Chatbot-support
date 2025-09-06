from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

# 1. User Detail Serializer
# --------------------------
# Used for returning user info (e.g., after registration or when fetching profile).
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "is_active", "date_joined"]


# 2. User Registration Serializer
# -------------------------------
# Used to create a new user account.
# Handles password hashing and sets default role if not provided.
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "role"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Ensure password is hashed
        user.save()
        return user


# 3. Custom Token Obtain Pair Serializer
# ---------------------------------------
# Extends SimpleJWT's default token serializer to include user info in login response.
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims (extra info in token payload)
        token["email"] = user.email
        token["role"] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Include additional user info in response
        data.update({
            "user": {
                "id": self.user.id,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "role": self.user.role,
            }
        })
        return data
