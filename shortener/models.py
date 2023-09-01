from django.db import models
from django.conf import settings
from django.utils import timezone

from random import choices
from string import ascii_letters
import uuid


class Link(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True, unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    original_link = models.URLField()
    shortened_link = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "shortened_links"
