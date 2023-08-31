# Standard library imports
from django.shortcuts import redirect, Http404
from django.conf import settings

# Third-party imports
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

# Local application imports
from .models import Link
from .serializer import LinkSerializer


class ShortenerListAPIView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class ShortenerCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LinkSerializer

    def create(self, request, *args, **kwargs):
        original_link = request.data.get('original_link')
        if not original_link:
            return Response({"detail": "Original link is required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        link = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class Redirector(generics.GenericAPIView):
    permission_classes = []
    def get(self, request, shortener_link, *args, **kwargs):
        shortener_link = settings.HOST_URL + '/' + shortener_link
        redirect_link = Link.objects.filter(shortened_link=shortener_link).first()
        if redirect_link:
            return redirect(redirect_link.original_link)
        else:
            raise Http404("Shortened link not found.")
