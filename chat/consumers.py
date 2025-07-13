import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from .models import ChatMessage ,OfferNegotiationMessage

from tendor.models import Tender
from offer.models import Offer

User = get_user_model()

class BaseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        self.other_user_id = self.scope['url_route']['kwargs']['user_id']

        self.room_name = f"chat_{min(str(self.user.id), str(self.other_user_id))}_{max(str(self.user.id), str(self.other_user_id))}"

        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))


    @database_sync_to_async
    def get_user_by_id(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        
    @database_sync_to_async
    def get_offer_by_id(self, offer_id):
        try:
            return Offer.objects.get(id=offer_id)
        except Offer.DoesNotExist:
            return None
    

    @database_sync_to_async
    def get_tender_by_id(self, tender_id):
        try:
            return Tender.objects.get(id=tender_id)
        except Tender.DoesNotExist:
            return None



class ChatConsumer(BaseConsumer):

    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        tender_id=data.get('tender')

        if self.user.id:
            sender = await self.get_user_by_id(self.user.id)
        else:
            await self.send(text_data=json.dumps({'error': "sender id is None"}))
            return
        
        if self.other_user_id:
            receiver = await self.get_user_by_id(self.other_user_id)
        else :
            await self.send(text_data=json.dumps({'error': 'receiver id is None'}))
            return

        tender=None

        if tender_id:
            tender = await self.get_tender_by_id(tender_id) or None

        print("tender_==>",tender)
        
       
        await self.save_message(sender,receiver,message,tender)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': str(sender.id),
                'tender': str(tender.id) if tender else None,
            }
        )

    @database_sync_to_async
    def save_message(self, sender, receiver, message,tender):
        return ChatMessage.objects.create(sender=sender, receiver=receiver, message=message,tender=tender)



class OfferNegotiationConsumer(BaseConsumer):

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        offer_id=data.get('offer')

        if self.user.id:
            sender = await self.get_user_by_id(self.user.id)
        else:
            await self.send(text_data=json.dumps({'error': "sender id is None"}))
            return
        
        if self.other_user_id:
            receiver = await self.get_user_by_id(self.other_user_id)
        else :
            await self.send(text_data=json.dumps({'error': 'receiver id is None'}))
            return
        
        offer=None
        
        if offer_id:
            offer = await self.get_offer_by_id(offer_id) or None

        print("offer type==>",type(offer))
       
        await self.save_message(sender,receiver,message,offer)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': str(sender.id),
                'offer': str(offer.id) if offer else None ,
            }
        )

    @database_sync_to_async
    def save_message(self, sender, receiver, message,offer):
        return OfferNegotiationMessage.objects.create(sender=sender, receiver=receiver, message=message,offer=offer)


