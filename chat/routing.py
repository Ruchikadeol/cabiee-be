from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/offer-negotiate/(?P<user_id>[0-9a-f-]+)/$', consumers.OfferNegotiationConsumer.as_asgi()),
    re_path(r'^ws/chat/(?P<user_id>[0-9a-f-]+)/$', consumers.ChatConsumer.as_asgi()),
]

