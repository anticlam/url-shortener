from django.urls import path
from shortener.views import LinkViewSet

app_name = 'my_shortener_app'

urlpatterns = [
    path('', LinkViewSet.as_view({'get': 'list'}), name='all_links'),
    path('create/', LinkViewSet.as_view({'post': 'create'}), name='create_api'),
]
