from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer

class IsSelfOrAdminPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it,
    or allow admin users to do anything.
    """
    def has_object_permission(self, request, view, obj):
        # Admin users can always perform any action
        if request.user and request.user.is_staff:
            return True
        
        # Write permissions are only allowed to the owner of the user profile
        if request.method in permissions.SAFE_METHODS:
            return True # Allow read-only access for everyone (GET)

        # Allow update/delete only if the user is editing their own profile
        return obj == request.user

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the view requires.
        """
        if self.action in ['list', 'create', 'destroy']:
            # Only staff can list all users or create/delete users
            permission_classes = [permissions.IsAdminUser]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            # Only the owner or an admin can retrieve/update a profile
            permission_classes = [IsSelfOrAdminPermission]
        else:
            permission_classes = [permissions.IsAuthenticated] # Default for safety

        return [permission() for permission in permission_classes]