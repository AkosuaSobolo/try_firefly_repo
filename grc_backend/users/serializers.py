from rest_framework import serializers
from .models import User
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Fields exposed for viewing by authenticated users
        fields = ('id', 'email', 'is_staff')
        # Fields that can be read but not changed in the API
        read_only_fields = ('id', 'email', 'date_joined', 'is_staff')

        

class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        # The fields Djoser will use for user creation
        fields = ('id', 'username', 'email', 'password') 