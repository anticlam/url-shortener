from django.db import models
from random import choices
from string import ascii_letters
from django.conf import settings

class Link(models.Model):
    original_link=models.URLField(max_length=2048)
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
