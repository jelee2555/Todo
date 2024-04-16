from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password, nickname):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=email, nickname=nickname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, nickname=None):
        superuser = self.create_user(
            email=email,
            password=password,
            nickname=nickname,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    nickname = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']
