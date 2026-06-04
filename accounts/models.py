from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for the real estate platform."""

    class UserType(models.TextChoices):
        BUYER = 'buyer', 'Buyer'
        AGENT = 'agent', 'Agent'
        ADMIN = 'admin', 'Admin'

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.BUYER,
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
