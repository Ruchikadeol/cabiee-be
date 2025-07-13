from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("get/", EmployeesView.as_view()),
    path('get-ride-details/',GetRideDetails.as_view()),
    path("get/<uuid:user_id>/",EmployeeDetails.as_view())
]
