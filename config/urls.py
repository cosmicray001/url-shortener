from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("url_shortener_app.urls")),
    path('django/admin/', admin.site.urls),
]
