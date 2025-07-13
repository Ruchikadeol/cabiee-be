from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("get-messages/<int:offer_id>/", OfferNegotiationHistory.as_view()),

]
