from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import redirect, Http404
from django.conf import settings

from .models import Link
from .serializer import LinkSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAdminUser]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = []
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        if self.action == 'list':
            return Link.objects.all()
        return Link.objects.none()

    def create(self, request, *args, **kwargs):
        original_link = request.data.get('original_link')
        if not original_link:
            return Response({"detail": "Original link is required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        link = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'], url_path='(?P<shortener_link>.+)')
    def redirector(self, request, shortener_link):
        shortener_link = settings.HOST_URL + '/' + shortener_link
        redirect_link = Link.objects.filter(shortened_link=shortener_link).first()
        if redirect_link:
            return redirect(redirect_link.original_link)
        else:
            raise Http404("Shortened link not found.")
