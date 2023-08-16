from django.shortcuts import redirect, render
from rest_framework.generics import ListAPIView,CreateAPIView

from django.http import Http404

from django.views import View
from django.conf import settings

from .models import Link
from .serializer import LinkSerializer

from rest_framework.decorators import APIView, api_view, permission_classes

from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from rest_framework.response import Response


class ShortenerListAPIView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset=Link.objects.all()
    serializer_class=LinkSerializer

class ShortenerCreateApiView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LinkSerializer

    def create(self, request, *args, **kwargs):
        original_link = request.data.get('original_link')
        existing_link = Link.objects.filter(original_link=original_link).first()

        if existing_link:
            serializer = self.get_serializer(existing_link)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
       
        return Response(serializer.data)
        
class Redirector(View):
    def get(self,request,shortener_link,*args, **kwargs):
        shortener_link=settings.HOST_URL+'/'+self.kwargs['shortener_link']
        redirect_link = Link.objects.filter(shortened_link=shortener_link).first()
        if redirect_link:
            redirect_link = redirect_link.original_link
            return redirect(redirect_link)
        else:
            raise Http404    