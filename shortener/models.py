from django.db import models
from random import choices
from string import ascii_letters
from django.conf import settings
import uuid
#import timezone
from django.utils import timezone

class Link(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    original_link=models.URLField()
    shortened_link=models.URLField(blank=True,null=True)


    def shortener(self):
        while True:
            random_string=''.join(choices(ascii_letters,k=6))
            new_link=settings.HOST_URL+'/'+random_string
    
            if not Link.objects.filter(shortened_link=new_link).exists():
                break

        return new_link

    def save(self, *args, **kwargs):
        existing_link = Link.objects.filter(original_link=self.original_link).first()
        if existing_link:
            self.pk = existing_link.pk
            self.shortened_link = existing_link.shortened_link
        else:
            if not self.shortened_link:
                new_link = self.shortener()
                self.shortened_link = new_link

        return super().save(*args, **kwargs)