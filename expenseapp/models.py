from django.db.models import CASCADE
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Expense(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.IntegerField()
    type=models.CharField(max_length=128)
    date=models.DateTimeField(auto_now_add=True)

class Income(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True,null=True)

class Limit(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.IntegerField()