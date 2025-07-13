from django.db import models
from django.contrib.postgres.fields import ArrayField
from user.models import User
import uuid
from django.contrib.postgres.fields import JSONField 


class Driver(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,  editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cabbie_profile')
    name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=10)
    address=models.JSONField(blank=True, null=True)
    vehicle_number=models.CharField(max_length=20)
    bank_account=models.CharField(max_length=15,blank=True, null=True)
    beneficiary_id=models.CharField(max_length=100,blank=True, null=True)
    ifsc=models.CharField(max_length=12,blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name