from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import SignUpSerializer
from .tokens import create_jwt_pair_for_user


USER_CREATED_SUCCESS = {"message": "User Created Successfully"}
ERROR_DURING_REGISTRATION = {"message": "Error during registration: {}"}
INVALID_CREDENTIALS = {"message": "Invalid credentials"}


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        """
        Create a new user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            return Response(
                {**USER_CREATED_SUCCESS, "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except IntegrityError as e:
            return Response(
                {**ERROR_DURING_REGISTRATION.format(str(e))},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_create(self, serializer):
        """
        Save the user data.
        """
        serializer.save()

    @action(detail=False, methods=["post"], name="user_login")
    def login(self, request):
        """
        Authenticate a user.
        """
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user:
            tokens = create_jwt_pair_for_user(user)
            return Response(
                {"message": "Authentication successful", "tokens": tokens},
                status=status.HTTP_200_OK,
            )
        return Response(INVALID_CREDENTIALS, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], name="retrieve_user_info")
    def retrieve_info(self, request):
        """
        Retrieve logged in user information.
        """
        content = {"user": str(request.user), "auth": str(request.auth)}
        return Response(content, status=status.HTTP_200_OK)
