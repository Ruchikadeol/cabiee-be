from django.urls import path
from .views import InitiatePayoutView

urlpatterns = [
    path("initiate/", InitiatePayoutView.as_view()),
]