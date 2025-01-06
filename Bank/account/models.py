from django.db import models
from django.contrib.auth.models import User
from .constant import AccountType,GenderType
# Create your models here.


class UserBankAccount(models.Model):
    user=models.OneToOneField(User,related_name='account',on_delete=models.CASCADE)
    accountType=models.CharField(max_length=10,choices=AccountType)
    accountNo=models.IntegerField(unique=True)
    birthDate=models.DateField(null=True,blank=True)
    gender=models.CharField(max_length=10,choices=GenderType)
    initialDepositDate=models.DateField(auto_now=True)
    balance=models.DecimalField(default=0,max_digits=12,decimal_places=2)

    def __str__(self):
        return str(self.accountNo)
    

class UserAddress(models.Model):
    user=models.OneToOneField(User,related_name='address',on_delete=models.CASCADE)
    street_address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    postalCode=models.IntegerField()
    country=models.CharField(max_length=100)


    def __str__(self):
        return str(self.user.email)
    
