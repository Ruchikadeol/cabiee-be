from django.db import models
from organisation.models import Organisation
import uuid
from user.models import User

class Admin(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='owner_profile')
    name=models.CharField(max_length=50)
    organisation=models.ForeignKey(Organisation,on_delete=models.SET_NULL,blank=True,null=True)
    phone_number=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name