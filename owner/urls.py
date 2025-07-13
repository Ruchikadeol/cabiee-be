from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("delete/<uuid:user_id>/", DeleteEmployee.as_view())
]
