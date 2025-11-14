from rest_framework import serializers
from .models import User
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    Only exposes safe/necessary fields for public viewing and updates.
    """
    class Meta:
        model = User
        # Fields exposed for viewing by authenticated users
        fields = ('id', 'email', 'is_staff')
        # Fields that can be read but not changed via the API
        read_only_fields = ('id', 'email', 'date_joined', 'is_staff')

        

class UserCreateSerializer(DjoserUserCreateSerializer):
    """
    Serializer used by Djoser for user registration (POST /api/auth/users/).
    It inherits all fields from Djoser's default user creation.
    """
    class Meta(DjoserUserCreateSerializer.Meta):
        # The fields Djoser will use for user creation
        fields = ('id', 'username', 'email', 'password') 
        # Add any other custom required fields here