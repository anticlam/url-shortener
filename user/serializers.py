import hashlib

from django.core.cache import cache

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate_email(self, value):
        # Generate a cache key based on the hashed email value
        cache_key = f"email_exists:{hashlib.md5(value.encode()).hexdigest()}"

        # Try to get the value from the cache
        email_exists = cache.get(cache_key)

        if email_exists is None:
            # If the cache doesn't have the value, query the database and set the cache
            email_exists = User.objects.filter(email=value).exists()
            cache.set(cache_key, email_exists, 60 * 15)  # Cache for 15 minutes

        if email_exists:
            raise ValidationError("Email has already been used")

        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user
