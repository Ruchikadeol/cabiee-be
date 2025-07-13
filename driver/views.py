from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from utils.permission import IsRoleAllowed
from user.serializers import UserSerializer
from .serializers import DriverSerializer
from tendor.serializers import TenderSerializer

from tendor.models import Tender
from driver.models import Driver
from user.models import User

class CabbieSignupView(APIView):

       def post(self, request):
        try:
            email=request.data.get("email")
            password=request.data.get("password")
            address=request.data.get('address')
            vehicle_number=request.data.get("vehicle_number")
            phone_number=request.data.get("phone_number")
            name=request.data.get("name")
            ifsc=request.data.get("ifsc")
            bank_account=request.data.get("bank_account")

            if not email or not password or not address or not vehicle_number or not phone_number or not name or  not bank_account or not ifsc:
                return Response({"success":False,"message":"All fields are required"},status=status.HTTP_400_BAD_REQUEST)
            
            signup_data = {"email":email,"password":password ,"role": 'driver'}

            signupSerializer = UserSerializer(data=signup_data)
            if signupSerializer.is_valid():
                user = signupSerializer.save()

                # coordinates = get_coordinates(request.data.get('address'))

                data={
                    "name" :name,
                    "phone_number" :phone_number,
                    "vehicle_number" :vehicle_number,
                    'address':address,
                    "user":str(user.id),
                    'ifsc':ifsc,
                    'bank_account':bank_account

                }
  
                serializer = DriverSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"success": True,"data":serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({"success": False, "message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
                
            return Response({"success": False, "message":signupSerializer.errors},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

# get all those tenders where teh timing does not clash with teh already accepted tenders
class GetTendorView(APIView):
    permission_classes = [IsRoleAllowed]
    allowed_roles=['driver']

    def get(self,request):
        try:
            user=request.user

            driver=Driver.objects.get(user=user.id)

            # fetch the tenders accepted by the logged in cabbie
            accepted_tenders=list(Tender.objects.filter(driver=driver.id))

            timings={'pickup_timing':[],'drop_timing':[]}

            for tender in accepted_tenders:
                timings["pickup_timing"].append(tender.pickup_timing)
                timings["drop_timing"].append(tender.drop_timing)

            # new tenders which arenot assigned to any cabbie yet
            new_tenders=list(Tender.objects.filter(driver__isnull=True,price__isnull=True))

            if len(timings['pickup_timing'])!=0 :
            # tenders which do not clash with the already accepted tenders
                filtered_tenders=[tender for tender in new_tenders if tender.pickup_timing not in timings['pickup_timing'] and tender.drop_timing not in timings['drop_timing'] ]
                new_tenders=filtered_tenders
                
            serializer=TenderSerializer(new_tenders,many=True)
            return Response({'success':True,"message":serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success':False,"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
