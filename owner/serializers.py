from rest_framework import serializers
from .models import Admin


class AdminSerializer(serializers.ModelSerializer):

    # id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Admin
        fields = ['name','organisation','user','phone_number']
        read_only_fields = ["organisation"]

        def to_representation(self,instance):

            return{'id':instance.user,"name":instance.name,'organisation':instance.organisation,'phone_number':instance.phone_number}

