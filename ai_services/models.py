"""
Models for AI Services — chat session storage.
"""

import uuid
from django.db import models
from django.conf import settings


class ChatSession(models.Model):
    """Represents a chatbot conversation session."""
    session_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chat_sessions',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ai_chat_sessions'
        verbose_name = 'Chat Session'
        verbose_name_plural = 'Chat Sessions'
        ordering = ['-updated_at']

    def __str__(self):
        user_str = self.user.username if self.user else 'Anonymous'
        return f"Chat {self.session_id} ({user_str})"


class ChatMessage(models.Model):
    """A single message within a chat session."""

    class Role(models.TextChoices):
        USER = 'user', 'User'
        MODEL = 'model', 'Model'

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_chat_messages'
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.role}] {self.content[:50]}..."
