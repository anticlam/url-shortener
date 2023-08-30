from django.contrib import admin
from django.urls import path, include 
from shortener.views import Redirector

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shortener/', include(('shortener.urls', 'my_shortener_app'), namespace='my_shortener_namespace')),
    path('<str:shortener_link>/', Redirector.as_view(), name='redirector'),

    # API routes
    path('api/users/', include('user.urls')),  # Note: We'll modify user.urls accordingly in the next step

    # Uncomment below if you want to keep the old route (without the API prefix) alongside the new one
    # path("user/", include("user.urls")),
]
