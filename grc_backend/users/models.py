from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra):
        if not username:
            raise ValueError("Username required")
        if not email: 
            raise ValueError("Email required")
            
        user = self.model(
            username=username, 
            email=self.normalize_email(email), **extra)
        user.set_password(password) 
        user.save(using=self._db)
        return user
        
    def create_superuser(self, username, email, password, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        
        if extra.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
            
        return self.create_user(username, email, password, **extra)

class User(AbstractBaseUser, PermissionsMixin):
    # primary identifier field
    username = models.CharField(max_length=150, unique=True)
    
    # Secondary identifier
    email = models.EmailField(unique=True)
    
    name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]