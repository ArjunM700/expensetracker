from django.db.models import CASCADE
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone # Import timezone

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    type = models.CharField(max_length=128)
    # Replaced auto_now_add with default
    date = models.DateTimeField(default=timezone.now)

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    # Replaced auto_now_add with default, kept null=True
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)
class Limit(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.IntegerField()