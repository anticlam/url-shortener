from django.contrib import admin
from django.urls import path, include
from shortener.views import LinkViewSet  
urlpatterns = [
    path('admin/', admin.site.urls),
    path('shortener/', include(('shortener.urls', 'my_shortener_app'), namespace='my_shortener_namespace')),
    path('<str:shortener_link>/', LinkViewSet.as_view({'get': 'redirector'}), name='redirector'),  # Update this line

    # API routes
    path('api/users/', include('user.urls')),

    # Uncomment below if you want to keep the old route (without the API prefix) alongside the new one
    # path("user/", include("user.urls")),
]
