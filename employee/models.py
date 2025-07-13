from django.db import models
import uuid
from organisation.models import Organisation
from user.models import User
from group.models import Group
from django.contrib.postgres.fields import JSONField 

class Employee(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,  editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='employee_profile')
    name=models.CharField(max_length=50)
    address=models.JSONField(blank=True, null=True)
    shift_timings=models.CharField(blank=True,null=True,default="9am-6pm",max_length=50)
    phone_number=models.CharField(max_length=10,blank=True,null=True)
    organisation=models.ForeignKey(Organisation,on_delete=models.CASCADE,related_name='organisation_employee')
    group=models.ForeignKey(Group,on_delete=models.SET_NULL,null=True,blank=True)
    is_deleted=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

   
    def __str__(self):
        return self.name
    