from django.db import models
import uuid
from django.contrib.postgres.fields import JSONField 

class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation_name = models.CharField(max_length=150, unique=True)
    address=models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organisation_name
