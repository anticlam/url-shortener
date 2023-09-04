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
    updated_at = models.DateTimeField(auto_now=True)  
    original_link = models.CharField(max_length=2048)
    shortened_link = models.CharField(
        max_length=100, blank=True, null=True, db_index=True
    ) 

    class Meta:
        db_table = "shortened_links"
