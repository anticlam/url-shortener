from shortener.views import ShortenerCreateApiView, ShortenerListAPIView
from django.urls import path, include

app_name = 'my_shortener_app'

urlpatterns = [
    path('',ShortenerListAPIView.as_view(),name='all_links'),
    path('create/',ShortenerCreateApiView.as_view(),name='create_api'),
]