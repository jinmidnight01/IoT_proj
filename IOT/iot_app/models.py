from email.policy import default
from django.db import models
from django.utils import timezone

# Create your models here.

class Congression(models.Model):
    num = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)