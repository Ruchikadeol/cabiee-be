from rest_framework import serializers
from .models import Tender,EmployeeTravelDetails,DriverTravelDetails,EmployeeTenderHistory
from employee.models import Employee
from goSwift import settings
from django.core.validators import MinValueValidator,MaxValueValidator

from offer.models import Offer

class TenderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    driver=serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Tender
        fields = ['id','organisation','price','driver',"pickup_timing","drop_timing",'expire',"company_share","pending_charges",'is_active','group_size','monthly_charges']
        read_only_fields = ['id'] 


    def to_representation(self,instance):

        employee_ids = list(EmployeeTenderHistory.objects.filter(tender=instance.id).values_list('employee',flat=True))
        employees=list(Employee.objects.filter(id__in=employee_ids).values('id','address','name'))
        members=len(employees)

        print("employees",employees)

        description=" "

        for employee in employees:
            description+=str(employee.get("name"))+" "

        pending_charges=int(instance.pending_charges)

        if members==0:
             monthly_rental=instance.monthly_charges + pending_charges

        else:    
            monthly_rental=instance.monthly_charges + (pending_charges/members)
        
        driver=str(instance.driver)
        if instance.driver:
            driver=str(instance.driver.id)


        offers=list(Offer.objects.filter(tender=instance.id).values('offered_price','driver'))
        print("offer")

        return {"id":instance.id,'organisation':str(instance.organisation),'price':instance.price,'driver':driver,'pending_charges':instance.pending_charges,
               "description":description,"monthly_rental":monthly_rental,"company_share":instance.company_share,'is_active':instance.is_active,'pickup_timing':instance.pickup_timing,"drop_timing":instance.drop_timing,'expire':instance.expire,'offers':offers}


class EmployeeTravelDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=EmployeeTravelDetails
        fields = ['id','date','employee','tender','pickup_timing','drop_timing']
        read_only_fields = ['id'] 
    
    def to_representation(self,instance):
         return {"date":instance.date,'employee':str(instance.employee.user.id),'tender':str(instance.tender.id),'pickup_timing':instance.pickup_timing,
               "drop_timing":instance.drop_timing}



class DriverTravelDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model=DriverTravelDetails
        fields = ['id','date','driver','tender','picked_employees','droped_employees']
        read_only_fields = ['id'] 


class EmployeeTenderHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model =EmployeeTenderHistory
        fields = ['id','tender','leaving_date','amount_paid']
        read_only_fields = ['id']