from django.db import models
from django.conf import settings


class Agent(models.Model):
    """Model representing a real estate agent."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agent_profile',
    )
    license_number = models.CharField(max_length=50, unique=True)
    agency_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    specializations = models.CharField(
        max_length=500,
        blank=True,
        help_text='Comma-separated specializations (e.g., residential, commercial)',
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agents'
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} — {self.agency_name}"

    @property
    def property_count(self):
        return self.properties.count()
