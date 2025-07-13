from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, date
from django.utils import timezone
from django.utils. timezone import localtime,now,make_aware
from utils.permission import IsRoleAllowed


from .serializers import TenderSerializer,EmployeeTravelDetailsSerializer,DriverTravelDetailSerializer
from employee.serializers import EmployeeSerializer
from group.models import Group
from .models import Tender,EmployeeTravelDetails,DriverTravelDetails,EmployeeTenderHistory
from employee.models import Employee
from driver.models import Driver

from owner.models import  Admin

class TenderView(APIView):

    permission_classes = [IsRoleAllowed]
    allowed_roles=['admin']

    def post(self,request):
        try:
            
            group_id=request.data.get('group')
            try:

                group=Group.objects.get(id=group_id)
                print("group==============>",group)
                
                employees=list(Employee.objects.filter(group=group))
                if not employees:
                    return Response({"success":False,'message':" NO EMPLOYEES IN GROUP "},status=status.HTTP_404_NOT_FOUND)

                print("employees==============>",employees)
                members=len(employees)
                description=" "

                for employee in employees:
                    description+=str(employee.name)+" "

                tender_data={
                    'organisation':group.organisation.id,
                    'group_size':members,
                    'description':description
                }
                print("tender_data==============>",tender_data)

                serializer=TenderSerializer(data=tender_data)
                if serializer.is_valid():
                    tender=serializer.save()
                    Group.objects.filter(id=group_id).delete()

                    for employee in employees:
                        EmployeeTenderHistory.objects.create(tender=tender,employee=employee)

                    return Response({"success":True,'data':serializer.data},status=status.HTTP_201_CREATED)
                return Response({"success":False,'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
      
            except Group.DoesNotExist:
                return Response({"success":False,'message':"GROUP NOT FOUND"},status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"success":False,"message":str(e)},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success":False,"message":str(e)},status=status.HTTP_404_NOT_FOUND)


    def get(self,request):

        user=request.user
        
        admin=Admin.objects.get(user=user.id)

        print("organisaton id ==========+>",admin.organisation.id)
        tenders=Tender.objects.filter(organisation=admin.organisation.id)

        if tenders !=None:
            serializer=TenderSerializer(tenders,many=True)
            return Response({"success":True,'data':serializer.data},status=status.HTTP_200_OK)

        return Response({"success":False,'message':"TENDERS NOT FOUND"},status=status.HTTP_404_NOT_FOUND)


class TenderEmployees(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,tender_id):
        
        try:
        
            tender=Tender.objects.get(id=tender_id ,is_active=True)

            employees_id=list(EmployeeTenderHistory.objects.filter(tender=tender,is_active_member=True).values_list("employee",flat=True))
            if len(employees_id)==0:
                return Response({"success":False,"message":"NO EMPLOYEES ARE THERE IN THIS TENDER"},status=status.HTTP_404_NOT_FOUND)

            employees=Employee.objects.filter(id__in=employees_id)
            serializer=EmployeeSerializer(employees,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Tender.DoesNotExist:
            return Response({"success":False,'message':"TENDER NOT FOUND"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success":False,"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TenderTravelDetailsView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,tender_id):
        try:
            print("tender_id==>",tender_id)
            tender=Tender.objects.get(id=str(tender_id))
            print("tender=========+++++>",tender)

            if not  tender:
                 return Response({"success":False,"message":"TENDER NOT  FOUND"},status=status.HTTP_404_NOT_FOUND)

            employees_travel_details=EmployeeTravelDetails.objects.filter(tender=tender_id)
            driver_travel_details=DriverTravelDetails.objects.filter(tender=tender_id)

            employee_serializer=EmployeeTravelDetailsSerializer(employees_travel_details,many=True)
            driver_serializer=DriverTravelDetailSerializer(driver_travel_details,many=True)

            data={
                'tender':tender_id,
                'company-location':tender.organisation.address,
                'employees-travel-details':employee_serializer.data,
                'driver-travel-details':driver_serializer.data
            }

            return Response({"success":True,"data":data},status=status.HTTP_200_OK)
        except Tender.DoesNotExist:
            return Response({"success":False,"message":"TENDER NOT FOUND"},status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"success":False,"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def update_tender_travel_details(tender_id,user_id,driver_id):
    try:

        employee = Employee.objects.get(user=user_id)
        driver=Driver.objects.get(user=driver_id)

        tender = Tender.objects.get(id=tender_id)

        tender_pickup_timing=make_aware(datetime.combine(date.today(), tender.pickup_timing))
        tender_drop_timing=make_aware(datetime.combine(date.today(), tender.drop_timing))
        current_time = localtime(now())

        pickup_timing_diff=abs(current_time-tender_pickup_timing)
        drop_timing_diff=abs(current_time-tender_drop_timing)

        employee_travel_details, emp_created = EmployeeTravelDetails.objects.get_or_create(
            tender=tender,
            employee=employee,
            date=date.today(),
            defaults={'pickup_timing': localtime(now())} if pickup_timing_diff<drop_timing_diff else {'drop_timing': localtime(now())}
        )

        if not emp_created:
            if pickup_timing_diff<drop_timing_diff:
                employee_travel_details.pickup_timing = localtime(now())
            else :
                employee_travel_details.drop_timing = localtime(now())

        driver_travel_details, driver_created = DriverTravelDetails.objects.get_or_create(
            tender=tender,
            driver=driver,
            date=date.today(),
            defaults={'picked_employees': True} if pickup_timing_diff<drop_timing_diff else {'droped_employees': True}
        )

        if not driver_created:
            if pickup_timing_diff<drop_timing_diff:
                driver_travel_details.picked_employees = True
            else :
                driver_travel_details.droped_employees = True

        driver_travel_details.save()
        employee_travel_details.save()
        
        return Response({"success": True, "message": "Travel details updated successfully."}, status=status.HTTP_200_OK)

    except Employee.DoesNotExist:
        return Response({"success": False, "message": "EMPLOYEE NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)
    except Driver.DoesNotExist:
        return Response({"success": False, "message": "DRIVER NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)
    except Tender.DoesNotExist:
        return Response({"success": False, "message": "TENDER NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("error===================++>",str(e))
        return Response({"success": False, "message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)