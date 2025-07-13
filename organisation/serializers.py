from rest_framework import serializers
from .models import Organisation


class OrganisationSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Organisation
        fields = ["id","organisation_name", "address"]
        read_only_fields = ['id']
