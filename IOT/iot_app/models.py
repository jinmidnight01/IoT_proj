from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Congression(models.Model):
    num = models.IntegerField(default=1)
    created_at = models.DateTimeField()

class Eat(models.Model):
    flag = models.BooleanField(default=True)
    eat_count = models.PositiveIntegerField(default=0)

class Menu(models.Model):
    lunch = models.CharField(max_length=500)
    dinner = models.CharField(max_length=500)