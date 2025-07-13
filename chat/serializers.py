from rest_framework import serializers
from .models import ChatMessage,OfferNegotiationMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'message', 'timestamp','tender']

class OfferNegotiationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferNegotiationMessage
        fields = ['id', 'sender', 'receiver', 'message', 'timestamp','offer']