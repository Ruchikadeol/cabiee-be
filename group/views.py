from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .utils.groupCreation import group_coordinates 
from goSwift import settings
from datetime import date
import calendar
from utils.permission import IsRoleAllowed

from employee.models import Employee 
from employee.serializers import EmployeeSerializer
from organisation.models import Organisation
from .serializers import GroupSerializer
from owner.models import Admin
from user.models import User
from .models import Group
from tendor.models import Tender ,EmployeeTenderHistory

from tendor.serializers import TenderSerializer ,EmployeeTenderHistorySerializer
from driver.models import Driver
from driver.serializers import DriverSerializer


class GroupsView(APIView):

    permission_classes = [IsRoleAllowed]
    allowed_roles=['admin']

    def post(self, request):
        try:
            user = request.user

            admin=Admin.objects.get(user=user.id)
            organisation=Organisation.objects.get(id=admin.organisation.id)

            if not organisation:
                return Response({'success': False, 'message': "ORGANISATION NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)         

            existing_groups=list(Group.objects.filter(organisation=organisation.id).values_list('id',flat=True))
            existing_group_employees=list(Employee.objects.filter(group__in=existing_groups).values_list('id',flat=True))
               
            #    all employees
            employees=list(Employee.objects.filter(organisation=organisation.id,is_deleted=False))
            active_tenders=list(Tender.objects.filter(organisation=organisation.id,is_active=True).values_list('id',flat=True))

            if active_tenders:

                active_employees=list(EmployeeTenderHistory.objects.filter(tender__in=active_tenders,is_active_member=True).values_list('employee',flat=True))
                employees=[emp for emp in employees if emp.id not in active_employees]

            new_employees=[emp for emp in employees if emp.id not in existing_group_employees]
                
            if len(new_employees)==0:
                return Response({"success":False,"message":"NO EMPOYEES TO GROUP"},status=status.HTTP_400_BAD_REQUEST)
            
            employee_address_list = [{'id': emp.id, 'latitude': float(emp.address.get('latitude')),'longitude': float(emp.address.get('longitude'))} for emp in employees]
            radius_km=float(settings.GROUP_RADIUS)

            clusters=group_coordinates(employee_address_list,radius_km)

            created_groups=[]

            for  cluster in clusters:
                group_data={'organisation':organisation.id}                    
                serializer=GroupSerializer(data=group_data)

                
                if serializer.is_valid():
                    new_group=serializer.save()

                    created_group=serializer.data

                    employees_id=[employee.get('id') for employee in cluster]
                    employees = list(Employee.objects.filter(id__in=employees_id))

                    created_group['group_size']=len(employees)
                    description=""

                    for employee in employees:
                        description+=employee.name+" "
                        employee.group=new_group
                        employee.save()

                    created_group['description']=description
                    created_groups.append(created_group)

                else:
                    return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            #  delete the ids of the existing group
            Group.objects.filter(id__in=existing_groups).delete()
                 
            return Response({"success": True, "data": created_groups}, status=status.HTTP_201_CREATED)
        except Organisation.DoesNotExist:
            return Response({'success': False, 'message': "ORGANISATION NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)         
        except Admin.DoesNotExist:
            return Response({'success': False, 'message': "ADMIN NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'success': False, 'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get(self,request):
        user = request.user
        print("user",user)

        admin=Admin.objects.get(user=user.id)
        organisation=str(admin.organisation.id)
            
        try:
            groups=list(Group.objects.filter(organisation=organisation))
            serializer=GroupSerializer(groups,many=True)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
                 return Response({'success': False, 'message':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


def calculate_pending_charges(monthly_charges,pending_charges):

    today= date.today()
    days_travelled = today.day -1
    total_days= calendar.monthrange(today.year, today.month)[1]
    total_charges=(monthly_charges+pending_charges)

    travelling_charges=(total_charges*days_travelled)/total_days
    pending_charges=total_charges-travelling_charges

    return {"travelling_charges":travelling_charges,"pending_charges":pending_charges}


class RemoveEmployee(APIView):
    permission_classes = [IsRoleAllowed]
    allowed_roles=['admin']
     
    def patch(self,request):
        try:

            user_id=request.data.get('employee')
            tender_id=request.data.get('tender')

            employee=Employee.objects.get(user=user_id,is_deleted=False)

            remaining_employees=len(list(EmployeeTenderHistory.objects.filter(tender=tender_id,is_active_member=True)))-1
            travelling_charges=None

            tender=Tender.objects.filter(id=tender_id,is_active=True).first()
            print("tender=======>",tender)

            if tender:

                charges=calculate_pending_charges(tender.monthly_charges,tender.pending_charges)
                print("charges================>",charges)

                tender.pending_charges+=charges.get('pending_charges')
                travelling_charges=charges.get('travelling_charges')
                tender.group_size=tender.group_size-1

                if remaining_employees<=0:
                    tender.is_active=False

                tender.save()
                #  employe group mapping make it isActive_member=false
                employee_tender_history=EmployeeTenderHistory.objects.filter(tender=tender_id,employee=str(employee.id),is_active_member=True).first()
                if not employee_tender_history:
                     return Response({"success":False,"message":"EMPLOYEE NOT FOUND IN THIS TENDER"},status=status.HTTP_404_NOT_FOUND)

                print("employee_tender_history=======>",employee_tender_history)

                data={
                    'is_active_member':False,
                    'leaving_date':date.today(),
                    'amount_paid':int(travelling_charges)
                }

                serializer=EmployeeTenderHistorySerializer(employee_tender_history,data=data)
                if serializer.is_valid():
                    serializer.save()
                    print("EmployeeTenderHistory========>",serializer.data)

                    return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)
                return Response({'success':False,"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST) 
        except User.DoesNotExist:
            return Response({"success":False,"message":"USER NOT FOUND "},status=status.HTTP_404_NOT_FOUND)
        except Employee.DoesNotExist:
            return Response({"success":False,"message":"EMPLOYEE NOT FOUND"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success':False,"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)      
         

class GroupDetailsView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,group_id):
        try:

            data={
                    'group':None,
                    'employees':None ,
                    'tender':None,
                    "driver":None
                }

            group=Group.objects.get(id=group_id)
            group_serializer=GroupSerializer(group)
            print("gruop===============++++>",group)

            data['group']= group_serializer.data
            print("gruop===============++++>",group_serializer.data)

            employees=list(Employee.objects.filter(group=group_id))

            if employees:
                employees_serializer=EmployeeSerializer(employees,many=True)
                data['employees']= employees_serializer.data

            return Response({"success":True,"data":data},status=status.HTTP_200_OK)

        except Group.DoesNotExist:
             return Response({"success":False,"message":"GROUP DOES NOT EXIST"},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"success":False,"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)