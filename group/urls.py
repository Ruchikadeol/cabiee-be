from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("create/", GroupsView.as_view()),
    path("get/",GroupsView.as_view()),
    path("remove-employee/",RemoveEmployee.as_view()),
    path("group-details/<uuid:group_id>",GroupDetailsView.as_view())
  
]

