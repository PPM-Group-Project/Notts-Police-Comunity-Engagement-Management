from django.db import models
  
class Representative (models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=100,null=False)
    lastName = models.CharField(max_length=100,null=False)
    eMail = models.EmailField(null=False)
    address = models.CharField(max_length=255,null=False)

class Community (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,null=False)
    description = models.CharField(max_length=255,default='')
    address = models.CharField(max_length=255,null=False)
    frequency = models.PositiveIntegerField(default = 0 , null = False)
    engagementStart = models.DateField(null = False)
    representative = models.ForeignKey(Representative,on_delete = models.SET_NULL, null = True)