from django.shortcuts import render
from .models import Organisation
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from employee.models import Employee
from employee.serializers import EmployeeSerializer
from .serializers import OrganisationSerializer
from rest_framework.permissions import IsAuthenticated
from owner.models import Admin
from utils.permission import IsRoleAllowed

from utils.exception_handler import exception_handler


# Create your views here.

class OrganisationView(APIView):
    permission_classes = [IsRoleAllowed]
    allowed_roles=['admin']

    def get(self,request):
        try:

            user=request.user
            admin=Admin.objects.get(user=user.id)
            data={'organisation':None,'employees':None}

            if admin.organisation:
                serializer=OrganisationSerializer(admin.organisation)
                data['organisation']=serializer.data

                employees=Employee.objects.filter(organisation=admin.organisation,is_deleted=False)

                if employees:
                    employee_serializer=EmployeeSerializer(employees,many=True)
                    data['employees']=employee_serializer.data

            return Response({"success":True,"data":data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success":False,"message":exception_handler(str(e))},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def patch(self,request):
        try:
            user=request.user
            admin=Admin.objects.get(user=user.id)            
            
            if not admin.organisation:
                return Response({"success":False,"message":"YOU HAVE NOT REGISTERED ANY ORGANISATION"},status=status.HTTP_401_UNAUTHORIZED)

            serializer=OrganisationSerializer(admin.organisation,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"success":True,"data":serializer.data},status=status.HTTP_201_CREATED)

            return Response({"success":False,"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Admin.DoesNotExist:
            return Response({"success":False,"message":"ADMIN NOT FOUND"},status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print("erorr====>",e)
            return Response({"success":False,"message":exception_handler(str(e))},status=status.HTTP_500_INTERNAL_SERVER_ERROR)