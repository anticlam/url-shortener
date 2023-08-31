from shortener.views import ShortenerCreateAPIView, ShortenerListAPIView
from django.urls import path, include

app_name = 'my_shortener_app'

urlpatterns = [
    path('',ShortenerListAPIView.as_view(),name='all_links'),
    path('create/',ShortenerCreateAPIView.as_view(),name='create_api'),
]