from django.db import models

# Create your models here.
class User(models.Model):
    Name    = models.CharField(max_length=255)    
    Mobile  = models.CharField(max_length = 255, unique=True,
                                error_messages = {'unique': 'A account already exists with this mobile number'})
    email   = models.EmailField(unique=True,
                                error_messages = {'unique': 'A account already exists with this mobile number'})
    id      = models.CharField(max_length=255, primary_key = True,
                                error_messages = {'primary_key': 'This user id is already taken'})
    passwd  = models.CharField(max_length=255)
    ques    = models.IntegerField()
    ans     = models.TextField()
    balence = models.CharField(max_length=20)
    leaf    = models.CharField(max_length=25)
    premium = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.Name

class Services(models.Model):
    Name    = models.CharField(max_length=100)
    price   = models.CharField(max_length=10)   #default : Indian Rupees.
    code    = models.CharField(max_length=20, primary_key=True,
                                error_messages = {'unique': 'Service code already exists'})
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.Name

class HelpDesk(models.Model):
    STATUS = (("Unanswered","unanswered"),("Answered","answered"))
    user_id = models.CharField(max_length=255)
    query = models.TextField()
    status = models.CharField( max_length=15,default='unanswered', choices = STATUS)
    token = models.CharField(max_length=20,unique = True)

    class Meta:
        verbose_name = 'HelpDesk'
        verbose_name_plural=verbose_name

