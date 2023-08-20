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

    def shortener(self):
        """
        Generate a unique short link.
        """
        while True:
            # Generate a random string of length 6 from ASCII letters
            random_string = ''.join(choices(ascii_letters, k=6))
            
            # Construct the full short link URL using the generated random string
            new_link = f"{settings.HOST_URL}/{random_string}"
    
            # Check if the generated short link already exists in the database
            # If not, return the new unique short link
            if not Link.objects.filter(shortened_link=new_link).exists():
                return new_link

    def save(self, *args, **kwargs):
        """
        Override save method to handle duplicate original links and generate short links.
        """
        
        # Check if a link with the same original URL already exists in the database
        existing_link = Link.objects.filter(original_link=self.original_link).first()

        # If the link already exists, just return without saving as it's a duplicate
        if existing_link:
            # Update the instance's attributes to match the existing link's attributes
            self.pk = existing_link.pk
            self.created_at = existing_link.created_at
            self.shortened_link = existing_link.shortened_link
            return

        # If the link does not exist and the shortened link is not set, generate a new short link
        if not self.shortened_link:
            self.shortened_link = self.shortener()

        # Call the parent class's save method to handle the actual saving to the database
        super().save(*args, **kwargs)
