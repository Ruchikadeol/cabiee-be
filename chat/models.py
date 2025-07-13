from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

from offer.models import Offer
from tendor.models import Tender

class OfferNegotiationMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.SET_NULL, blank=True, null=True)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, blank=True, null=True)
    offer=models.ForeignKey(Offer, related_name='offer', on_delete=models.SET_NULL, blank=True, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']


class ChatMessage(models.Model):
    sender = models.ForeignKey(User,related_name='sent_message',on_delete=models.SET_NULL, blank=True, null=True)
    receiver = models.ForeignKey(User,related_name='received_message',on_delete=models.CASCADE, blank=True, null=True)
    tender=models.ForeignKey(Tender, related_name='tender_message', on_delete=models.SET_NULL, blank=True, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']