from django.core.validators import EmailValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import Argon2PasswordHasher, make_password


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email field must be specified')
        if not password:
            raise ValueError('The password field must be specified')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password=password, is_superuser=True)
        user.is_staff = True
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, **extra_fields):
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_admin = False
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, validators=[EmailValidator])
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_valid_until = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email


