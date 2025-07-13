from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import ChatMessage,OfferNegotiationMessage
from .serializers import ChatMessageSerializer,OfferNegotiationMessageSerializer


class ChatHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,other_user_id):

        user=request.user

        try:
            chats=ChatMessage.objects.filter(sender=user.id, receiver_id=other_user_id) | ChatMessage.objects.filter(sender_id=other_user_id, receiver=user.id)

            serializer=ChatMessageSerializer(chats,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"success":False,"message":str(e)},status=status.HTTP_400_BAD_REQUEST)

class OfferNegotiationHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,offer_id):

        try:
            chats=OfferNegotiationMessage.objects.filter(offer=offer_id)
            serializer=OfferNegotiationMessageSerializer(chats,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"success":False,"message":str(e)},status=status.HTTP_400_BAD_REQUEST)


