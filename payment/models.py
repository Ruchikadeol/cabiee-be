# models.py
from django.db import models
from user.models import User

class P2PPayment(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_payments")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed")
    ], default="PENDING")

    reference_id = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.sender} paid {self.receiver} ₹{self.amount}"

