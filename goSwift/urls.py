from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path("user/", include("user.urls")),
    path("employee/", include("employee.urls")),
    path("group/", include("group.urls")),
    path('cabbie/',include('driver.urls')),
    path('tender/',include('tendor.urls')),
    path('offer/',include('offer.urls')),
    path('chat/',include('chat.urls')),
    path('otp/',include('otp.urls')),
    path('organisation/',include('organisation.urls')),
    path("owner/",include('owner.urls')),
     path("payment/",include('payment.urls')),

]
