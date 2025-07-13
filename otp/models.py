from django.db import models
from user.models import User

class OTP(models.Model):
    id=models.AutoField(primary_key=True)
    otp=models.CharField(max_length=6)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    expires_at=models.DateTimeField()


    def __str__(self):
        return self.otp

