import random
from django.utils import timezone

def generate_otp(length=6):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp

def check_if_valid(otp):
    current_time=timezone.now()
    if  current_time<= otp.expires_at:
        return True
    return False