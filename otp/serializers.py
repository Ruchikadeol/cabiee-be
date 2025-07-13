from rest_framework import serializers
from .models  import OTP


class OTPSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=OTP
        fields=['otp','user','expires_at']