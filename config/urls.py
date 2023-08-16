
from django.contrib import admin
from django.urls import path, include 

from shortener.views import Redirector



urlpatterns = [
    path('admin/', admin.site.urls),
    path('shortener/', include(('shortener.urls', 'my_shortener_app'), namespace='my_shortener_namespace')),
    path('<str:shortener_link>/',Redirector.as_view(),name='redirector'),
    path("auth/", include("user.urls")),
    # user
    #path('user/', include(('user.urls', 'user_app'), namespace='user_api')),
]
