from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path("get/",OrganisationView.as_view()),
    path("update/",OrganisationView.as_view())

]