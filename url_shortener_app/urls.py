from django.urls import path
from url_shortener_app.views.views import HomePage, URLDecode

urlpatterns = [
    path('', HomePage.as_view(), name='home-page'),
    path('<str:short_url>/', URLDecode.as_view(), name='url-decode'),
]
