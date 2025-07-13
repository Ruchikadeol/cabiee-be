from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
                                                                                        
from utils.permission import IsRoleAllowed
from utils.exception_handler import exception_handler
from tendor.serializers import TenderSerializer,EmployeeTenderHistory
from .serializers import EmployeeSerializer,RideDetailsSerializer
from .models import Employee
from user.models import User
from owner.models import Admin
from organisation.models import Organisation
from group.models import Group
from tendor.models import Tender


class EmployeesView(APIView):

    permission_classes = [IsRoleAllowed]
    allowed_roles=['admin']

    def get(self, request):
        try:
            user=request.user   
            print("user id======>",user.id)

            admin=Admin.objects.get(user=user.id)
            print("admin===============>",admin)

            print("admin Organisation==========+>",admin.organisation)

            if admin.organisation:
                print("organisation emp=====>",admin.organisation.organisation_employee.all())
                employees=list(admin.organisation.organisation_employee.filter(is_deleted=False))
                if len(employees)==0:
                    return Response(
                        {"success": True, "data":[]},
                        status=status.HTTP_200_OK,
                    )
                
                serializer = EmployeeSerializer(employees, many=True)
                data=serializer.data
                return Response({"success": True, "data": serializer.data},status=status.HTTP_200_OK)
            return Response({"success": True, "data": []},status=status.HTTP_200_OK)

        except Exception as e:
            print("error==================>",e)
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetRideDetails(APIView):
    permission_classes = [IsRoleAllowed]
    allowed_roles=['employee']

    def get(self,request):

        try:
            user=request.user

            employee=Employee.objects.get(user=user.id)
            print(" empployee profile",user.employee_profile.all())

            active_tender=EmployeeTenderHistory.objects.get(employee=employee ,is_active_member=True)
            tender=active_tender.tender

            driver=tender.driver

            extra_charges=tender.pending_charges/tender.group_size
            monthly_rental=tender.monthly_charges+extra_charges

            ride_details={
                'driver':driver,
                'location':employee.address.get('address'),
                'timing':tender.pickup_timing,
                'monthly_rental':monthly_rental,
                'vehicle_number':driver.vehicle_number
            }

            serializer=RideDetailsSerializer(ride_details)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except EmployeeTenderHistory.DoesNotExist:
            return Response({"success":False,"message":"NO CABBIE ALLOTTED YET"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success":False,"message":exception_handler(str(e))},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# 
class EmployeeDetails(APIView):

    permission_classes=[IsAuthenticated]
    allowed_roles=['employee','admin']

    
    def get(self,request,employee_id):
        try:

            employee=Employee.objects.get(user=employee_id,is_deleted=False)
            print("employee============+>",employee)
            
            data={
                'id':employee.user.id,
                'email':employee.user.email
            }

            employee_serializer=EmployeeSerializer(employee)
            employee_data=employee_serializer.data
            employee_data.pop('id')

            data = {**data, **employee_data}

            tender_ids=list(EmployeeTenderHistory.objects.filter(employee=employee).values_list('tender',flat=True))

            employee_tenders=list(Tender.objects.filter(id__in=tender_ids))
            if employee_tenders:
                    tender_serializer=TenderSerializer(employee_tenders)
                    data['tender']=tender_serializer.data
            
            return Response({"success":True,"data":data},status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"success":False,"message":"EMPLOYEE NOT FOUND"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("e===========>",e)
            return Response({"success":False,"message":exception_handler(str(e))},status=status.HTTP_500_INTERNAL_SERVER_ERROR)