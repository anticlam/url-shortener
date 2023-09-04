from django.conf import settings
from django.shortcuts import redirect, Http404
from django.core.cache import cache
from rest_framework import viewsets, status, throttling
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Link
from .serializer import LinkSerializer

CACHE_TIMEOUT = 3600  # 1 hour


class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer
    throttle_classes = [throttling.UserRateThrottle]

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [IsAdminUser]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = []
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        if self.action == "list":
            return Link.objects.all()
        return Link.objects.none()

    def create(self, request, *args, **kwargs):
        original_link = request.data.get("original_link")
        if not original_link:
            return Response(
                {"detail": "Original link is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Try to get the shortened link from cache
        cached_data = cache.get(original_link)
        if cached_data:
            return Response(cached_data, status=status.HTTP_201_CREATED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        link = serializer.save()

        # Cache data
        cache.set(original_link, serializer.data, CACHE_TIMEOUT)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"], url_path="(?P<shortener_link>.+)")
    def redirector(self, request, shortener_link):
        shortener_link = f"{settings.HOST_URL}/api/redirect/{shortener_link}"

        # Try to get the original link from cache
        original_link = cache.get(shortener_link)
        if original_link:
            return redirect(original_link)

        redirect_link = Link.objects.filter(shortened_link=shortener_link).first()
        if redirect_link:
            # Cache original link
            cache.set(shortener_link, redirect_link.original_link, CACHE_TIMEOUT)
            return redirect(redirect_link.original_link)
        else:
            raise Http404("Shortened link not found.")
