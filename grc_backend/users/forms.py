from django.contrib.auth.forms import UserChangeForm, BaseUserCreationForm
# from django import forms
from .models import User 

# 1. Form used for creating a user in the Admin (Add User view)
class CustomUserCreationForm(BaseUserCreationForm):
    """
    A form for creating new users in the admin.
    Inherits from BaseUserCreationForm to handle custom fields.
    """
    class Meta:
        model = User
        # Define fields explicitly, using 'email' and 'name'
        fields = ('email', 'name') 

# 2. Form used for editing an existing user in the Admin (Change User view)
class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating existing users in the admin.
    """
    class Meta:
        model = User
        # Define the fields, ensuring 'email' and 'name' are present
        fields = ('email', 'name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')