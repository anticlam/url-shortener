# Importing Django's authentication function
from django.contrib.auth import authenticate

# Importing DRF's classes and constants
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

# Handling database integrity errors
from django.db.utils import IntegrityError

# Local imports
from .serializers import SignUpSerializer
from .tokens import create_jwt_pair_for_user

class SignUpView(generics.GenericAPIView):
    # Specifying the serializer for user sign up
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        # Getting the data from the request
        data = request.data
        # Initializing the serializer with the request data
        serializer = self.serializer_class(data=data)
        
        # Checking if the serializer data is valid
        if serializer.is_valid():
            try:
                # Trying to save the user
                serializer.save()
                
                # Preparing success response
                response_data = {"message": "User Created Successfully", "data": serializer.data}
                return Response(data=response_data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                # Handling case where email is already used
                response_data = {"message": "Email has already been used"}
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
        
        # Returning any serialization errors
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        # Retrieve email and password
        email = request.data.get("email")
        password = request.data.get("password")
        
        # Authenticating the user with the provided credentials
        user = authenticate(email=email, password=password)
        
        if user is not None:
            # User authenticated successfully, generating JWT tokens
            tokens = create_jwt_pair_for_user(user)
            response = {"message": "Login Successful", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            # Handling failed authentication
            return Response(data={"message": "Invalid email or password"})

    def get(self, request: Request):
        # Response with user and authentication details
        content = {"user": str(request.user), "auth": str(request.auth)}      
        return Response(data=content, status=status.HTTP_200_OK)
