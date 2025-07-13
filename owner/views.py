from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from user.models import User
from employee.models import Employee
from tendor.models import Tender,EmployeeTenderHistory

class DeleteEmployee(APIView):

    def delete(self,request,user_id):
        try:
            employee=Employee.objects.get(user=user_id)

            tender=EmployeeTenderHistory.objects.filter(employee=employee,is_active_member=True).first()
            if tender:
                return Response({"success":False,"message":f"CAN'T DELETE EMPLOYEE.ACTIVE MEMBER OF THE TENDER WITH TENDER ID {tender_id}.REMOVE EMPLOYEE FROM THE GROUP THEN TRY AGAIN"},status=status.HTTP_400_BAD_REQUEST)

            if employee.group:
                employee.group=None
            employee.is_deleted=True
            employee.save()
           
            return Response({"success":True,"message":"EMPLOYEE DELETED"},status=status.HTTP_200_OK)

        except Employee.DoesNotExist:
            return Response({"success":False,"message":"Employee NOT FOUND"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("error==================>",e)
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )