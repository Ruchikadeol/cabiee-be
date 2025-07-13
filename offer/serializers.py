from rest_framework import serializers
from .models import Offer

class OffferSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Offer
        fields = ['id','tender','offered_price','driver']
        read_only_fields = ['id']