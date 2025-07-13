from django.db import models
from tendor.models import Tender
from user.models import User

class Offer(models.Model):
    id=models.AutoField(primary_key=True)
    offered_price=models.IntegerField()
    tender=models.ForeignKey(Tender,on_delete=models.CASCADE)
    driver=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return str(self.id)


