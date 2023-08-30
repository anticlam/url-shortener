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

    #validate email is not in use already    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email has already been used")
        return value

    def create(self, validated_data):
        # Create a new user, hash their password, and generate an authentication token.
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user

