from django.db import models
from django.utils import timezone
from datetime import timedelta,time
from organisation.models import Organisation
from group.models import Group
from driver.models import Driver
import uuid
from django.core.validators import MinValueValidator,MaxValueValidator
from employee.models import Employee

class Tender(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    driver=models.ForeignKey(Driver,on_delete=models.SET_NULL,blank=True,null=True,related_name='driver_tender')
    organisation=models.ForeignKey(Organisation,on_delete=models.CASCADE,related_name='organisation_tendor')
    price=models.IntegerField(blank=True,null=True)
    pickup_timing=models.TimeField(default=time(18, 0))
    group_size=models.IntegerField(blank=True,null=True)
    drop_timing=models.TimeField(default=time(9, 0))
    employees=models.ManyToManyField('Tender',through='EmployeeTenderHistory')
    company_share=models.IntegerField(default=50,validators=[MinValueValidator(1),MaxValueValidator(100)])
    pending_charges=models.IntegerField(default=0)
    monthly_charges=models.IntegerField(default=0)
    description=models.CharField(max_length=500,blank=True,null=True)
    is_active=models.BooleanField(default=True)
    expire=models.DateTimeField(default=timezone.now() + timedelta(days=30))
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.id)

class EmployeeTravelDetails(models.Model):
    id=models.AutoField(primary_key=True)
    date=models.DateTimeField(auto_now_add=True)
    tender=models.ForeignKey(Tender,on_delete=models.CASCADE,blank=True,null=True)
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE,blank=True,null=True)
    pickup_timing=models.DateTimeField(blank=True,null=True)
    drop_timing=models.DateTimeField(blank=True,null=True)
 
class DriverTravelDetails(models.Model):
    id=models.AutoField(primary_key=True)
    date=models.DateTimeField(auto_now_add=True)
    tender=models.ForeignKey(Tender,on_delete=models.CASCADE,blank=True,null=True)
    driver=models.ForeignKey(Driver,on_delete=models.CASCADE,blank=True,null=True)
    picked_employees=models.BooleanField(default=False)
    droped_employees=models.BooleanField(default=False)

class EmployeeTenderHistory(models.Model):
    id=models.AutoField(primary_key=True)
    tender=models.ForeignKey(Tender,on_delete=models.SET_NULL,blank=True,null=True)
    employee=models.ForeignKey(Employee,on_delete=models.SET_NULL,blank=True,null=True)
    leaving_date=models.DateField(blank=True,null=True)
    amount_paid=models.IntegerField(default=0)
    is_active_member=models.BooleanField(default=True)
  