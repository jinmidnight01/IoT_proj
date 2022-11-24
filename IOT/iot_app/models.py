from email.policy import default
from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)

class Congression(models.Model):
    num = models.IntegerField(default=1)
    created_at = models.DateTimeField()
    like = models.ManyToManyField(User, related_name='likes', blank=True)
    like_count = models.PositiveIntegerField(default=0)

