from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUserManager(BaseUserManager):
    """Custom manager for the User model."""
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a new superuser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    """Custom User model with email as main authentication."""
    email = models.EmailField(max_length=80, unique=True, blank=False,null=False)
    username = models.CharField(max_length=45, blank=False)
    date_of_birth = models.DateField(null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username