from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# A custom form set to display and manage User model fields in the Admin
class CustomUserAdmin(BaseUserAdmin):
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Fields to display on the main admin list page
    list_display = ('email', 'name', 'is_staff', 'is_active', 'last_login')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'name')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)