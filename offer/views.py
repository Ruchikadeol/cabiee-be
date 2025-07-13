from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.permission import IsRoleAllowed

from .serializers import OffferSerializer
from tendor.serializers import TenderSerializer
from .models import Offer
from tendor.models import Tender
from driver.models import Driver

class OfferView(APIView):
    permission_classes = [IsRoleAllowed]
    allowed_roles=['driver']

    def post(self,request):
        try:
            user=request.user

            tender=request.data.get('tender')
            existing_offer=Offer.objects.filter(driver=user.id,tender=tender).first()
            if existing_offer:
                return Response({'success':False,"message":"YOU HAVE ALREADY CREATED AN OFFER"},status=status.HTTP_400_BAD_REQUEST)

            data={
                'tender':tender,
                'offered_price':request.data.get('price'),
                'driver':user.id
            }
            
            serializer=OffferSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'success':True,"data":serializer.data},status=status.HTTP_201_CREATED)
                return Response({'success':False,"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success':False,"message":str(e)},status=status.HTTP_400_BAD_REQUEST)


    def patch(self,request):
        try:
            new_price=request.data.get('price')
            tender_id=request.data.get('tender')

            existing_tender=Tender.objects.get(id=tender_id)
            existing_offer=Offer.objects.get(tender=tender_id)

            if new_price!=None:
                existing_offer.offered_price=new_price
                existing_offer.save()
                return Response({"success":True,"message":"OFFER UPDATED"},status=status.HTTP_201_CREATED)

        except Tender.DoesNotExist:
            return Response({"success":False,"message":"TENDER DOES NOT EXIST"},status=status.HTTP_404_NOT_FOUND)
        except Offer.DoesNotExist:
            return Response({"success":False,"message":"OFFER DOES NOT EXIST"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success":False,"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AcceptOfferView(APIView):
    permission_classes = [IsRoleAllowed]
    allowed_roles=['admin']

    def post(self,request):
        try:

            tender=request.data.get('tender')
            cabbie_user=request.data.get('driver')
            price=request.data.get('offered_price')

            driver=Driver.objects.filter(user=cabbie_user).first()

            tender=Tender.objects.get(id=tender)
            tender.price=price
            tender.driver=driver

            price=int(price)
            monthly_rental=(price*(100-tender.company_share))/(100*tender.group_size)
            tender.monthly_charges=monthly_rental
            
            tender.save()

            serializer=TenderSerializer(tender)
            return Response({'success':True,"data":serializer.data},status=status.HTTP_202_ACCEPTED)

        except Driver.DoesNotExist:
            return Response({"success":False,"message":"Driver DOES NOT EXIST"},status=status.HTTP_404_NOT_FOUND)
        except Tender.DoesNotExist:
            return Response({"success":False,"message":"TENDER DOES NOT EXIST"},status=status.HTTP_404_NOT_FOUND)
        except Offer.DoesNotExist:
            return Response({"success":False,"message":"OFFER DOES NOT EXIST"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success":False,"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


