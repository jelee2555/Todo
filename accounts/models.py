from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    nickname = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'nickname']


