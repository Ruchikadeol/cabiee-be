from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("admin_signup/",AdminSignupView.as_view()),
    path('employees_onboard/',EmployeesOnboardView.as_view()),
    path("company_registration/", OrganisationRegistrationView.as_view()),
    path("login/", LoginView.as_view()),
    path("update/<uuid:user_id>/",UpdateEmployeeeView.as_view())
]
