from django.db import models
from django.conf import settings


class Inquiry(models.Model):
    """Model representing an inquiry about a property."""

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        READ = 'read', 'Read'
        RESPONDED = 'responded', 'Responded'
        CLOSED = 'closed', 'Closed'

    property = models.ForeignKey(
        'properties.Property',
        on_delete=models.CASCADE,
        related_name='inquiries',
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_inquiries',
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inquiries'
        verbose_name = 'Inquiry'
        verbose_name_plural = 'Inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry from {self.name} about {self.property.title}"
