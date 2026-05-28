from django.urls import include, path

from .views import api

urlpatterns = [
    path("", include((api.urls[0], api.urls[1]), namespace=api.urls[2])),
]