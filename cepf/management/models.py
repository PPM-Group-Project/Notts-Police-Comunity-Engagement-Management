from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Roles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    isOfficerManager = models.BooleanField(default=False)
    isDepartmentManager = models.BooleanField(default=False)
    isEventManager = models.BooleanField(default=False)
    def getAllRoles(self):
        roles = []
        if self.isOfficerManager : roles.insert("ofMan")
        if self.isDepartmentManager : roles.insert("depMan")
        if self.isEventManager : roles.insert("evMan")
        return roles


