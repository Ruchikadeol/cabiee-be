from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from utils.permission import IsRoleAllowed

from .serializers import UserSerializer, LoginSerializer
from organisation.serializers import OrganisationSerializer
from organisation.serializers import Organisation
from employee.serializers import EmployeeSerializer
from owner.serializers import AdminSerializer
from .models import User
from owner.models import Admin
from utils.exception_handler import exception_handler
from employee.models import Employee


class LoginView(APIView):

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data["user"]
                role=user.role

                refresh = RefreshToken.for_user(user)

                data={
                    "user":serializer.data,
                    f"{role}":None
                }
                print("user id============>",user.id)
                
                if role=='admin':
                    admin=Admin.objects.get(user=str(user.id))
                    print("admin============>",admin)
                    admin_serializer=AdminSerializer(admin)
                    admin_data= admin_serializer.data
                    admin_data.pop('user')
                    data[role]=admin_data
                    
                return Response({"success": True,"data":{**data,"tokens":{"access": str(refresh.access_token),"refresh": str(refresh)}}},status=status.HTTP_200_OK)

            return Response({"success": False, "message": exception_handler(str(serializer.errors))},status=status.HTTP_400_BAD_REQUEST)
        except Admin.DoesNotExist:
            return Response({"success": False, "message":"ADMIN NOT FOUND"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("error============++++++>",e)
            return Response(
                {"success": False, "message": exception_handler(str(e))},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class AdminSignupView(APIView):
    def post(self, request):
        try:
             
            email=request.data.get("email")
            password=request.data.get("password")
            phone_number=request.data.get("phone_number")
            name=request.data.get("name")
            missing_fields = []

            if not email:
                missing_fields.append('email')
            if not password:
                missing_fields.append('password')
            if not phone_number:
                missing_fields.append('phone_number')
            if not name:
                missing_fields.append('name')

            if missing_fields:
                return Response(
                    {"success": False, "message": f"The following fields are required: {', '.join(missing_fields)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            signup_data = {
                "email": email,
                "password": password,
                "role":"admin"
            }

            signupSerializer = UserSerializer(data=signup_data)
            if signupSerializer.is_valid(raise_exception=True):
                user = signupSerializer.save()

                admin_data={
                    "name":name,
                    "user":user.id,
                    "phone_number":phone_number,   
                }

                adminSerializer=AdminSerializer(data=admin_data)
                if adminSerializer.is_valid(raise_exception=True):
                    adminSerializer.save()                    
                    return Response({"success": True, "data":adminSerializer.data},status=status.HTTP_201_CREATED)
                
                return Response({"success":False,"message":exception_handler(str(adminSerializer.errors))},status=status.HTTP_400_BAD_REQUEST)
            return Response({"success":False,"message":exception_handler(str(signupSerializer.errors))},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:

            print("error================>",e)
            return Response(
                {"success": False, "error":exception_handler(str(e))},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class EmployeesOnboardView(APIView):
   permission_classes = [IsRoleAllowed]
   allowed_roles=['admin']

   def post(self,request):
    try:
        user=request.user

        email=request.data.get("email")
        password=request.data.get("password")
        address=request.data.get('address')
        phone_number=request.data.get("phone_number")
        name=request.data.get("name")
        shift_timings=request.data.get("shift_timings")


        if not email or not password or not address or not  phone_number or not name:
                return Response({"success":False,"message":"All fields are required"},status=status.HTTP_400_BAD_REQUEST)
 
        try:
            admin=Admin.objects.get(user=user.id)
        except Admin.DoesNotExist:
            return Response({"success":False,"message":"USER NOT FOUND"},status=status.HTTP_400_BAD_REQUEST)

        organisation=admin.organisation
        if not organisation:
            return Response({"success":False,"message":"ORGANISATION NOT FOUND"},status=status.HTTP_400_BAD_REQUEST)
        signup_data={
            "email" : email,
            "password" : password,
            'role':"employee"
        }

        user_serializer=UserSerializer(data=signup_data)
        if user_serializer.is_valid(raise_exception=True):
            new_user=user_serializer.save()

            employee_data={
                "user":new_user.id,
                "name":name,
                "phone_number":phone_number,                
                "organisation":organisation.id,
                "address":address,
                "shift_timings":shift_timings
            }

            employee_serializer=EmployeeSerializer(data=employee_data)
            if employee_serializer.is_valid(raise_exception=True):
                employee_serializer.save()
                return Response({"success":True,"data":employee_serializer.data},status=status.HTTP_201_CREATED)
                    
            return Response({"success":False,"message":exception_handler(str(employee_serializer.errors))},status=status.HTTP_400_BAD_REQUEST)
        return Response({"success":False,"message":exception_handler(str(user_serializer.errors))},status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({"success":False,"message":"USER NOT FOUND"},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"success":False,"message":exception_handler(str(e))},status=status.HTTP_400_BAD_REQUEST)


class OrganisationRegistrationView(APIView):

    permission_classes = [IsRoleAllowed]
    allowed_roles=['admin']
    
    def post(self, request):
        try:
            user=request.user

            admin=Admin.objects.filter(user=user.id).first()

            if not admin:
                return Response({"success":False,"message":"ADMIN NOT FOUND"},status=status.HTTP_404_NOT_FOUND)

            organisation=admin.organisation
            if organisation:
                return Response({"success":False,"message":"ORGANISATION ALREADY EXISTS"},status=status.HTTP_400_BAD_REQUEST)

            data = {
                "address": request.data.get('address'),
                "organisation_name": request.data.get("organisation_name")
            }
            serializer = OrganisationSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                organisation=serializer.save()

                admin.organisation=organisation
                admin.save()
                return Response({"success": True, "data":serializer.data},status=status.HTTP_201_CREATED)
            
            return Response({"success": False, "message":exception_handler(str(serializer.errors))},status=status.HTTP_400_BAD_REQUEST)   
        except Exception as e:
             return Response({"success":False,"message":exception_handler(str(e))},status=status.HTTP_400_BAD_REQUEST)


class UpdateEmployeeeView(APIView):
    permission_classes = [IsRoleAllowed]
    allowed_roles=['admin','employee']

    def patch(self,request,user_id):
        try:
            user=request.user
            user=User.objects.get(id=user_id)

            employee=Employee.objects.get(user=user_id)
            print("employee=============>",employee)

            data = {
                'name': request.data.get('name', employee.name),
                'phone_number': request.data.get('phone_number', employee.phone_number),
                'address': request.data.get('address', employee.address),
                'shift_timings': request.data.get('shift_timings', employee.shift_timings),
            }
            print("data=====++>",data)

            employee_serializer=EmployeeSerializer(employee,data=data,partial=True)

            if employee_serializer.is_valid(raise_exception=True):
                employee_serializer.save()

                return Response({"success":True,"message":employee_serializer.data},status=status.HTTP_200_OK)
           
        except Employee.DoesNotExist:
            return Response({"success":False,"message":"Employee NOT FOUND"},status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"success":False,"message":"User NOT FOUND"},status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print("e=====++>",e)
            return Response({"success":False,"message":exception_handler(str(e))},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 

