from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.permissions  import IsAuthenticated
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from utils.otp_utils import generate_otp,check_if_valid
from tendor.views import  update_tender_travel_details,EmployeeTenderHistory

from .serializers import OTPSerializer
from employee.models import Employee

from .models import OTP


def delete_otp(otp_code):
    try:
        otp=OTP.objects.get(otp=otp_code)
        otp.delete()

    except OTP.DoesNotExist:
            return Response({"success":False,"message":" OTP NOT FOUND"},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            return Response({"success":False,'message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class OTPView(APIView):
    permission_classes=[IsAuthenticated]

    def  get(self,request):
        try:
            user=request.user
            otp = generate_otp()
            data={
                'otp':otp,
                'user':str(user.id),
                'expires_at':datetime.now() + timedelta(minutes=5)
            }
            serializer=OTPSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"success":True,'data':serializer.data},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success":False,'message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self,request):
        try:
            user=request.user  

            if user.role!='driver':
                return Response({"success":False,"message":"UNAUTHORISED REQUEST"},status=status.HTTP_401_UNAUTHORIZED)

            otp_code=request.data.get('otp')
            otp=OTP.objects.get(otp=otp_code)
            
            is_otp_valid=check_if_valid(otp)

            employee=Employee.objects.filter(user=str(otp.user.id)).first()
            tender=EmployeeTenderHistory.objects.filter(employee=employee,is_active_member=True).first()
            tender=str(tender.id)

            if is_otp_valid:
                response=update_tender_travel_details(tender,otp.user,user.id)
                delete_otp(otp_code)
                return Response({"success":True,'message':"OTP MATCHED"},status=status.HTTP_200_OK)
            return Response({"success":False,'message':"OTP EXPIRED"},status=status.HTTP_400_BAD_REQUEST)
   
        except OTP.DoesNotExist:
            return Response({"success":False,"message":"INVALID OTP"},status=status.HTTP_400_BAD_REQUEST)


