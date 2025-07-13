from rest_framework import serializers
from .models import Group
from employee.models import Employee
from tendor.models import Tender


class GroupSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Group
        fields = ['id','organisation','created_at','updated_at']
        read_only_fields = ['id']


    def to_representation(self,instance):

        employees=list(Employee.objects.filter(group=instance.id))
        members=len(employees)

        description=" "
        status='Pending'

        for employee in employees:
            description+=str(employee.name)+" "

        print("description==>",description)
        
        return {"id":instance.id,'organisation':str(instance.organisation.id),'group_size':members,
               "description":description,'status':status,"created_at":instance.created_at,"updated_at":instance.updated_at}
