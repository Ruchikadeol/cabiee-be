from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'user', 'name', 'address','phone_number','organisation','shift_timings']
        read_only_fields = ['id']
        
        extra_kwargs = {'user': {'write_only': True}}

    def validate(self, data):
        user = data.get('user')
        phone_number=data.get('phone_number')
        address=data.get('address')

        if Employee.objects.filter(user=user).exists():
            raise serializers.ValidationError("This user is already assigned as an employee.")
        
        if len(phone_number)>10 or len(phone_number)<10:
            raise serializers.ValidationError("Phone number should be of 10 digits")
        
        if type(address)==str:
             raise serializers.ValidationError("Address must be an object conatning latitide and longitude")

        if address:
            required_keys = {'latitude', 'longitude'}
            if  required_keys.issubset(address.keys()):

                if address.get('latitude')=="" or  address.get('latitude')=="":
                    raise serializers.ValidationError("Address must contain latitude and longitude")
        else :
            data.pop('address')

        return data

    def create(self, validated_data):
        return Employee.objects.create(**validated_data)

    def to_representation(self,instance):
        user=instance.user
        
        return {"id":user.id,"name":instance.name,'email':user.email, 'address':instance.address,'phone_number':instance.phone_number,
        'shift_timings':instance.shift_timings}


class RideDetailsSerializer(serializers.Serializer):
    driver=serializers.CharField(max_length=100)
    location=serializers.CharField(max_length=200)
    timing=serializers.TimeField()
    monthly_rental=serializers.IntegerField()
    vehicle_number=serializers.CharField(max_length=200)