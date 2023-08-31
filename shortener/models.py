# Django model and utility imports
from django.db import models
from django.conf import settings
from django.utils import timezone

# Standard library imports
from random import choices
from string import ascii_letters
import uuid

class Link(models.Model):
    """
    Model for the link that will be shortened.
    """

    # Fields for the Link model
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)  # UUID as a primary key
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when the object is created
    original_link = models.URLField()  # Field to store the original URL
    shortened_link = models.URLField(blank=True, null=True)  
    """Field to store the shortened URL. It is set to blank and null as it will be generated automatically. 
    Not setting it as null causes an "It is impossible to change a nullable field 'shortened_link' on link to non-nullable without providing a default. This is because the database needs something to populate existing rows."
    error."""
    
    class Meta:
        db_table = "shortened_links"
 