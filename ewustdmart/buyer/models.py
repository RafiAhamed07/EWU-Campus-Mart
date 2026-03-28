from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# Create your models here.
class CustomeUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not (email.endswith("@std.ewubd.edu") or email.endswith("@ewubd.edu")):
            raise ValueError("The email must be a valid EWU email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(primary_key=True , editable=False , default=uuid.uuid4)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # role flag
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    # shop name (nullable because not all users are sellers)
    shop_name = models.CharField(max_length=100, blank=True, null=True)

    objects = CustomeUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
