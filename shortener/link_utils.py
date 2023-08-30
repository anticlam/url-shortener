from random import choices
from string import ascii_letters
from django.conf import settings

def shortener(LinkQuerySet):
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
        if not LinkQuerySet.filter(shortened_link=new_link).exists():
            return new_link
