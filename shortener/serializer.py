from hashlib import sha256
from random import choices
from string import ascii_letters, digits

from django.conf import settings
from django.core.cache import cache
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Link

CACHE_TIMEOUT = 3600  # 1 hour

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ("original_link", "shortened_link")

    def validate_original_link(self, value):
        validator = URLValidator()
        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid URL!")
        return value

    def create(self, validated_data):
        original_link = validated_data.get("original_link")

        # Check cache
        cached_data = cache.get(original_link)
        if cached_data:
            return Link(**cached_data)  # remake link from cache

        # Hashing and collision check
        while True:
            random_element = "".join(
                choices(ascii_letters + digits, k=2)
            )  # Random element to minimize likelihood of collision
            hash_obj = sha256((original_link + random_element).encode())
            random_string = hash_obj.hexdigest()[:6]
            new_link = f"{settings.HOST_URL}/api/redirect/{random_string}"

            link, created = Link.objects.get_or_create(
                shortened_link=new_link, defaults={"original_link": original_link}
            )

            if created or link.original_link == original_link:
                break

        # Cache the serialized data for future requests
        serialized_data = self.to_representation(link)
        cache.set(original_link, serialized_data, CACHE_TIMEOUT)

        return link
