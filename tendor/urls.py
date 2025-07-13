from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("create/",TenderView.as_view()),
    path("get/",TenderView.as_view()),
    path("employees-details/<uuid:tender_id>/",TenderEmployees.as_view()),
    path('travel-details/<uuid:tender_id>/',TenderTravelDetailsView.as_view()),

]
