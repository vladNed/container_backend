from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password

from users.models.constants import ROLE_TYPES

from rest_framework.authtoken.models import Token


class ContainerUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_password(self, password: str) -> str:
        if len(password) < 8:
            raise ValueError('Password must have at least 8 characters')

        check_upper_case = [
            ch.isupper()
            for ch in password
        ]

        if not any(check_upper_case):
            raise ValueError('Password must have one upper letter')

        return make_password(password, salt='conti', hasher='pbkdf2_sha1')

    def _create_user(self, email: str, password: str, **extra_fields) -> AbstractUser:
        if not email:
            raise ValueError('Email value must be given')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email: str, password: str, **extra_fields) -> AbstractUser:
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_admin', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields) -> AbstractUser:
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', 'AD')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, **extra_fields)


class ContainerUser(AbstractUser):
    '''
    Custom user for container app.
    It includes the email and roles
    '''
    username = None
    email = models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    data_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(choices=ROLE_TYPES, null=False, max_length=2, default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ContainerUserManager()

    def __str__(self) -> str:
        return f'{self.email} - {self.role}'

    def has_perm(self, perm, obj=None) -> bool:
        return self.is_superuser

    def has_module_perms(self, app_label) -> bool:
        return self.is_superuser
