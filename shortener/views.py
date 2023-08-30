# Standard library imports
from django.shortcuts import redirect, render
from django.http import Http404
from django.conf import settings
from django.views import View

# Third-party imports
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

# Local application imports
from .models import Link
from .serializer import LinkSerializer



class ShortenerListAPIView(ListAPIView):
    """API view to list all shortened links (Admin only)."""
    permission_classes = [IsAdminUser]
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

class ShortenerCreateApiView(CreateAPIView):
    """API view to create a shortened link."""
    permission_classes = [IsAuthenticated]
    serializer_class = LinkSerializer

    def create(self, request, *args, **kwargs):
        # Ensure the original link is provided in the request data
        original_link = request.data.get('original_link')
        
        if not original_link:
            return Response({"detail": "Original link is required."}, status=400)

        # Use the custom manager's method to get or create the link
        link, created = Link.objects.get_or_create_link(original_link)

        # Serialize the link object for the response
        serializer = self.get_serializer(link)
        return Response(serializer.data)

    

class Redirector(View):
    # View to redirect a user based on the shortened link.
    def get(self,request,shortener_link,*args, **kwargs):
        shortener_link=settings.HOST_URL+'/'+self.kwargs['shortener_link']
        redirect_link = Link.objects.filter(shortened_link=shortener_link).first()
        if redirect_link:
            return redirect(redirect_link.original_link)
        else:
            raise Http404("Shortened link not found.")   