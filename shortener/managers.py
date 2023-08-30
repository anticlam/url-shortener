from django.db import models
from .link_utils import shortener

class LinkManager(models.Manager):

    def get_or_create_link(self, original_link):
        # Check if a link with the same original URL already exists in the database
        existing_link = self.filter(original_link=original_link).first()

        if existing_link:
            return existing_link, False

        # If the link does not exist, generate a new short link and create a new Link instance
        shortened_link = shortener(self)
        link = self.create(original_link=original_link, shortened_link=shortened_link)
        return link, True
