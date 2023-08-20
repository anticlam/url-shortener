from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    #validate email is not in use already    
    def validate(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email has already been used")
        return email

    def create(self, validated_data):
        # Create a new user, hash their password, and generate an authentication token.
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user

