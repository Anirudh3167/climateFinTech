from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

#########################################
# BASIC CLIMATE FIN TECH MODELS
#########################################
class User_Details(AbstractUser):
    Name        = models.CharField(max_length=255,blank=True)
    Mobile      = models.CharField(max_length=255,blank=True)
    AccountType = models.CharField(max_length=255,default="Basic")
    Leaf        = models.CharField(max_length=255,default="0")
    Bio         = models.TextField(default="A Rapyd green user")
    Job         = models.CharField(max_length=255,default="Not Specified")

    REQUIRED_FIELDS: list()
    def __str__(self):
        return self.username
    class Meta:
          verbose_name = 'User_Details'
          verbose_name_plural=verbose_name

class HelpDesk(models.Model):
    STATUS      = (("Unanswered","unanswered"),("Answered","answered"))
    UserId      = models.CharField(max_length=255, unique = True)
    query       = models.TextField()
    status      = models.CharField( max_length=15,default='unanswered', choices = STATUS)
    token       = models.CharField(max_length=20,unique = True)

    class Meta:
        verbose_name = 'HelpDesk'
        verbose_name_plural=verbose_name

################################################
# FIN TECH MODELS
################################################
class Transactions(models.Model):
    trans_id = models.CharField(max_length=255,primary_key=True)
    sender     = models.ForeignKey(User_Details,on_delete=models.CASCADE)
    reciever   = models.CharField(max_length=255)
    currency    = models.CharField(max_length=5)
    date        =  models.DateTimeField(timezone.now())
    class Meta:
        verbose_name = 'Transactions'
        verbose_name_plural=verbose_name


#################################################
# BLOGS MODELS
#################################################
class Blogs(models.Model):
    Author = models.ForeignKey(User_Details,on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255,blank=False)
    content = models.TextField()
    views  =  models.CharField(max_length=100,blank=True)
    pay   =   models.CharField(max_length=5,blank=True)    
    class Meta:
        verbose_name = 'Blogs'
        verbose_name_plural=verbose_name

################################################
# SOTRE MODELS
################################################

class Lables(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        verbose_name = 'Lables'
        verbose_name_plural=verbose_name

class Products(models.Model):
    Product_Name = models.CharField(max_length=255)
    Product_title = models.CharField(max_length=255)
    Product_desc = models.TextField()
    Product_price = models.CharField(max_length=10)
    Stock = models.CharField(max_length=10)
    Lables = models.ManyToManyField(Lables)
    class Meta:
        verbose_name = 'Products'
        verbose_name_plural=verbose_name

class CartItems(models.Model):
    owner = models.ForeignKey(User_Details,on_delete=models.DO_NOTHING,related_name='owner')
    code = models.ForeignKey(Products,on_delete=models.DO_NOTHING,related_name='code')
    qty = models.CharField(max_length=10)
    status = models.CharField(max_length=5,default="ordered")  #i.e. Ordered and Delivered
    ordered_date = models.DateTimeField(timezone.now())
    class Meta:
        verbose_name = 'CartItems'
        verbose_name_plural=verbose_name

################################################
# CLIMATE TECH MODELS
################################################
class records(models.Model):
    User = models.ForeignKey(User_Details,on_delete=models.DO_NOTHING)
    result = models.CharField(max_length=255)
    param1 = models.CharField(max_length=30,blank=True)
    param2 = models.CharField(max_length=30,blank=True)
    param3 = models.CharField(max_length=30,blank=True)
    date    = models.DateTimeField(timezone.now())
    class Meta:
        verbose_name = 'records'
        verbose_name_plural=verbose_name
