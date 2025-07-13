# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import P2PPayment
from .utils.token_authentication import transfer_to_user,add_beneficiary,transfer_status
from user.models import User
from driver.models import Driver
from owner.models import Admin
from rest_framework import status
import random


class InitiatePayoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.user
        receiver_id = request.data.get("receiver_id")
        amount = request.data.get("amount")

        receiver=User.objects.filter(id=receiver_id).first()
        if not receiver:
            return Response({"error": "Receiver not found"}, status=400)

        receiver_profile=Driver.objects.filter(user=receiver_id).first()
        sender_profile=Admin.objects.filter(user=str(sender.id)).first()

        bank_account = receiver_profile.bank_account 
        ifsc = receiver_profile.ifsc
        
        if not receiver_profile.beneficiary_id:
            add_beneficiary_response=add_beneficiary(receiver_profile)
            if add_beneficiary_response.get("status") != "SUCCESS":
                return Response({
                    "success":False,
                    "message": "Failed to add beneficiary",
                    "details": add_beneficiary_response
                },status=status.HTTP_400_BAD_REQUEST)
            
            id=f"user{str(receiver_profile.user.id)}"
            id=id.replace('-','')
            receiver_profile.beneficiary_id=id
            receiver_profile.save()

        id=receiver_profile.beneficiary_id

        random_number = random.randint(10000, 99999)
        transfer_data={
            "transfer_id": f"tx_{str(random_number)}",
            "transfer_amount": float(amount),
            "beneficiary_details": {
                "beneficiary_id":id
            }
        }


        transfer_to_user_response = transfer_to_user(transfer_data)

        if not transfer_to_user_response or "status" not in transfer_to_user_response:
            return Response({
                "success":False,
                "message": "Transfer failed",
                "details": transfer_to_user_response
            }, status=status.HTTP_400_BAD_REQUEST)
        
        transfer_id=transfer_data.get('transfer_id')

        response=transfer_status(transfer_data.get('transfer_id'))
        
        payment_status = "PENDING"
        if response.get("status") == "SUCCESS":
            payment_status = "SUCCESS"
        elif response.get("status") == "FAILED":
            payment_status = "FAILED"

        payment = P2PPayment.objects.create(
            sender=sender,
            receiver=receiver,
            amount=amount,
            status=payment_status,
            reference_id=response.get("transfer_id"),
            remarks=payment_status
        )

        return Response({"success":True,'data':{
            "success":True,
            "cashfree_response": response
        }},status=status.HTTP_200_OK)
