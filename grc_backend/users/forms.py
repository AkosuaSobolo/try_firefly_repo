from django.contrib.auth.forms import UserChangeForm, BaseUserCreationForm
# from django import forms
from .models import User 

# 1. Form used for creating a user in the Admin (Add User view)
class CustomUserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name') 

# 2. Form for editing an existing user in the Admin
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')