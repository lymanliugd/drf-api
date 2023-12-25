from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    """Model Note."""

    user = models.ForeignKey(
        to=User,
        verbose_name='User',
        related_name='notes',
        on_delete=models.CASCADE,
    )

    content = models.TextField(
        verbose_name='Content',
    )

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
