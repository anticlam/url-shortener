from django.contrib import admin
from django.urls import path, include

from shortener.views import LinkViewSet

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/shortener/",
        include(
            ("shortener.urls", "my_shortener_app"), namespace="my_shortener_namespace"
        ),
    ),
    path(
        "api/redirect/<str:shortener_link>/",
        LinkViewSet.as_view({"get": "redirector"}),
        name="redirector",
    ),
    path("api/users/", include("user.urls")),
]
