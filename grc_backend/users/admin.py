# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# A custom form set to display and manage your User model fields in the Admin
class CustomUserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the forms inherited from BaseUserAdmin.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}), # Include the 'name' field
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Fields to display on the main admin list page
    list_display = ('email', 'name', 'is_staff', 'is_active', 'last_login')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'name')
    ordering = ('email',)

    # We do not include the 'date_joined' field in fieldsets because it's managed 
    # automatically, but we display 'last_login' to help manage users.


# Register your custom User model with the custom admin class
admin.site.register(User, CustomUserAdmin)