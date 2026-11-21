from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
import uuid
from users_accounts.models.custom_user_manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # 👤 Identity
    name = models.CharField(
        max_length=100,
    )

    surname = models.CharField(
        max_length=100,
        blank=True,
    )

    email = models.EmailField(
        unique=True,
    )

    # 🎂 Profile
    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True,
    )

    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
    )

    cover = models.ImageField(
        upload_to="users/covers/",
        blank=True,
        null=True,
    )

    skills = models.JSONField(
        default=list,
        blank=True,
    )

    # ⚙️ Account
    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_online = models.BooleanField(
        default=False,
    )

    # 📊 Future OS metrics
    task_count = models.PositiveIntegerField(
        default=0,
    )

    date_joined = models.DateTimeField(
        default=timezone.now,
    )

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.name} {self.surname}".strip()

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None

    @property
    def cover_url(self):
        if self.cover:
            return self.cover.url
        return None
