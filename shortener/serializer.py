from rest_framework import serializers
from .models import Link
from random import choices
from string import ascii_letters
from django.conf import settings

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('original_link', 'shortened_link')

    def create(self, validated_data):
        original_link = validated_data.get('original_link')
        
        # Logic for shortener
        while True:
            random_string = ''.join(choices(ascii_letters, k=6))
            new_link = f"{settings.HOST_URL}/{random_string}"
            if not Link.objects.filter(shortened_link=new_link).exists():
                break

        link = Link.objects.create(
            original_link=original_link, 
            shortened_link=new_link
        )
        return link
