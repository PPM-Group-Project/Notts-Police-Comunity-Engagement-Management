from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    # unique department id
    id = models.AutoField(primary_key=True)
    # department name
    departmentName = models.CharField(max_length=50, default="")
    # responsible officer , User object from django.contrib.auth.models
    responsibleOfficer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    # description of the department
    departmentDescription = models.CharField(max_length=100, default="")
    # privileges of if events in the department
    isOfficerManager = models.BooleanField(default=False)
    isDepartmentManager = models.BooleanField(default=False)
    isCommunityManager = models.BooleanField(default=False)
    isEventManager = models.BooleanField(default=False)


class UserDetails(models.Model):
    # User object from django.contrib.auth.models
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    # department that officer is part of, declared above
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    # additional user details for the officer
    badgeNumber = models.CharField(max_length=20, default="")
    # communities that the officer is in charge
    # communities = models.CharField(max_length=100, default="")
    # functions to retreive privileges that user has declared in Department

    def isOfficerManager(self):
        try:
            if self.department.isOfficerManager:
                return True
        except:
            return False
        return False

    def isDepartmentManager(self):
        try:
            if self.department.isDepartmentManager:
                return True
        except:
            return False
        return False

    def isCommunityManager(self):
        try:
            if self.department.isCommunityManager:
                return True
        except:
            return False
        return False

    def isEventManager(self):
        try:
            if self.department.isEventManager:
                return True
        except:
            return False
        return False

def setupDb():
    superuser = User()
    superuser.username = "superuser"
    superuser.set_password("superuser")
    superuser.first_name = "Super"
    superuser.last_name = "User"
    superuser.email = "ivica-matic@outlook.com"
    superuser.save()

    superDepartment = Department()
    superDepartment.departmentName = "Superusers"
    superDepartment.departmentDescription = "Default department for super users"
    superDepartment.responsibleOfficer = superuser
    superDepartment.isCommunityManager = superDepartment.isDepartmentManager = superDepartment.isEventManager = superDepartment.isOfficerManager = True
    superDepartment.save()

    superUserDetails = UserDetails()
    superUserDetails.user = superuser
    superUserDetails.department = superDepartment
    superUserDetails.save()

    officerDepartment = Department()
    officerDepartment.departmentName = "Officers"
    officerDepartment.departmentDescription = "Department for officers without prvilege on system"
    officerDepartment.responsibleOfficer = superuser
    officerDepartment.save()

