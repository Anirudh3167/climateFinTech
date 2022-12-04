from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User_Details(AbstractUser):
    Name        = models.CharField(max_length=255,null=True)
    Mobile      = models.CharField(max_length=255,null=True)
    AccountType = models.CharField(max_length=255,default="Basic")
    Leaf        = models.CharField(max_length=255,default="0")
    Bio         = models.TextField(default="A Rapyd green user")


class Services(models.Model):
    Name        = models.CharField(max_length=100)
    price       = models.CharField(max_length=10)   #default : Indian Rupees.
    code        = models.CharField(max_length=20, primary_key=True,
                                error_messages = {'unique': 'Service code already exists'})
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.Name

class HelpDesk(models.Model):
    STATUS      = (("Unanswered","unanswered"),("Answered","answered"))
    UserId      = models.CharField(max_length=255, unique = True)
    query       = models.TextField()
    status      = models.CharField( max_length=15,default='unanswered', choices = STATUS)
    token       = models.CharField(max_length=20,unique = True)

    class Meta:
        verbose_name = 'HelpDesk'
        verbose_name_plural=verbose_name

class Items(models.Model):
    Name = models.CharField(max_length=150)
    desc = models.TextField()
    code = models.CharField(max_length=50, primary_key = True)
    price = models.CharField(max_length=15)
    stock = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Items'
        verbose_name_plural=verbose_name

class CartItems(models.Model):
    code = models.CharField(max_length=50, primary_key = True)
    qty = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'CartItems'
        verbose_name_plural=verbose_name
