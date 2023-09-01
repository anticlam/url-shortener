from hashlib import sha256
from random import choices
from string import ascii_letters, digits

from django.conf import settings
from django.core.cache import cache
from rest_framework import serializers

from .models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ("original_link", "shortened_link")

    def create(self, validated_data):
        original_link = validated_data.get("original_link")
        # Check cache first
        cached_link = cache.get(original_link)
        if cached_link:
            return cached_link
        # Hashing and collision check
        while True:
            random_element = "".join(
                choices(ascii_letters + digits, k=2)
            )  # random element to minimize likelihood of collision
            hash_obj = sha256((original_link + random_element).encode())
            random_string = hash_obj.hexdigest()[:6]
            new_link = f"{settings.HOST_URL}/api/redirect/{random_string}"

            link, created = Link.objects.get_or_create(
                shortened_link=new_link, defaults={"original_link": original_link}
            )

            if created or link.original_link == original_link:
                break

        cache.set(original_link, link)
        return link
