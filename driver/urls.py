from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("get-tenders/", GetTendorView.as_view()),
    path("signup/",CabbieSignupView.as_view()),
]

