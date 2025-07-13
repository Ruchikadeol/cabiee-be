from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("create/", OfferView.as_view()),
    path("update/", OfferView.as_view()),
    path('accept/',AcceptOfferView.as_view())
]

