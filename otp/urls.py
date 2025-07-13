from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("get/", OTPView.as_view()),
    path('verify/',OTPView.as_view())
]

