from rest_framework import serializers
from .models import Driver


class DriverSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Driver
        fields = ['id', 'user', 'name', 'address', 'phone_number',"vehicle_number",'bank_account','ifsc']
        read_only_fields = ['id']


    def to_representation(self,instance):
        user=instance.user
        
        return {"id":user.id,"name":instance.name, 'address':instance.address,'phone_number':instance.phone_number,
        'vehicle_number':instance.vehicle_number,'ifsc':instance.ifsc,'bank_account':instance.bank_account}


