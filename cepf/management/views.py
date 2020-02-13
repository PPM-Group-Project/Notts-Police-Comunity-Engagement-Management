#from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import loader
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ObjectDoesNotExist
#from django.contrib.auth.forms import UserCreationForm
from .models import UserDetails, Department
from django.contrib.auth.models import User


def notAuthorisedPage(request):
    return HttpResponse("You are not authorised to access this property!")

def loginUser(request):
    template = loader.get_template('login.html')
    context = {}

    if (request.user.is_authenticated):
        return redirect(dashboard)
     

    if request.method =='GET':
        return HttpResponse(template.render(context,request))
    else:
        try:
            username = request.POST.get('username')
            passwd = request.POST.get('password')
            user = authenticate(username = username, password = passwd)
            login(request,user)
            return redirect(dashboard)
        except AttributeError:
            context["invalidLogin"] = True
            return HttpResponse(template.render(context,request))
    
def logoutUser(request):
    logout(request)
    return redirect(loginUser)

def dashboard(request):
    template = loader.get_template('personalDetails.html')
    context = {} 
    if (request.user.is_authenticated == False):
        return redirect(loginUser)
    return HttpResponse(template.render(context,request))

def officers(request):
    if isUserOfficerManager(request) == False : return redirect(notAuthorisedPage)
    template = loader.get_template('officers.html')
    listOfDepartments = Department.objects.all()
    listOfOfficers = UserDetails.objects.all()
    context = {}
    context["departments"] = listOfDepartments
    context["officers"] = listOfOfficers
    return HttpResponse(template.render(context,request))
 

def addOfficer(request):
    if isUserOfficerManager(request) == False : return redirect(notAuthorisedPage)
    if request.method == 'POST':
        try :
            firstName = request.POST.get('officerName')
            lastName = request.POST.get('officerSurname')
            eMail = request.POST.get('officereMail')
            username = request.POST.get('officerUsername')
            badgeNumber = request.POST.get('officerBadgeNumber')
            department = request.POST.get('department')
            communities = request.POST.get('communities')
            user = User()
            user.username = username
            user.first_name = firstName
            user.last_name = lastName
            user.set_password("default")
            user.email = eMail
            details = UserDetails()
            details.user = user
            details.badgeNumber = badgeNumber
            details.department = Department.objects.get(departmentName = department)
            user.save()
            details.save()
        except:
            return redirect(officers(request))
    
    return redirect(officers)    


def departments(request):
    if isUserOfficerManager(request) == False : return redirect(notAuthorisedPage)
    template = loader.get_template('departments.html')
    context = {} 
    context["officers"] = UserDetails.objects.all()
    context ["departments"] = Department.objects.all()
    for dep in context["departments"]:
        x = Department.objects.get(id = dep.id)
        dep.count = UserDetails.objects.filter(department = x).count()

    return HttpResponse(template.render(context,request))

def addDepartment(request):
    if isUserDepartmentManager(request) == False : return redirect(notAuthorisedPage)
    if request.method =='POST':
        try:
            dep = Department()
            dep.departmentName = request.POST.get('departmentName')
            dep.responsibleOfficer = User.objects.get(id = request.POST.get('officerInCharge'))
            dep.departmentDescription = request.POST.get('departmentDescription')
            if request.POST.get('isOfficerManager') : dep.isOfficerManager = True
            if request.POST.get('isDepartmentManager') : dep.isDepartmentManager = True
            if request.POST.get('isEventManager') : dep.isEventManager = True
            dep.save()
        except:
            return redirect(departments)
    return redirect(departments)


def isUserOfficerManager(request):
    #default piece of code for user autenthication on operation
    currentUserId = request.user.id
    if currentUserId == None : return False
    try:
        currentUser = User.objects.get(id = currentUserId)
        #change parameter below to check for different privilege
        if UserDetails.objects.get(user = currentUser).isOfficerManager:
            #logic starts
            return True
            #logic ends
    except ObjectDoesNotExist:
        return False

def isUserDepartmentManager(request):
    #default piece of code for user autenthication on operation
    currentUserId = request.user.id
    if currentUserId == None : return False
    try:
        currentUser = User.objects.get(id = currentUserId)
        #change parameter below to check for different privilege
        if UserDetails.objects.get(user = currentUser).isDepartmentManager:
            #logic starts
            return True
            #logic ends
    except ObjectDoesNotExist:
        return False

def isUserEventManager(request):
    #default piece of code for user autenthication on operation
    currentUserId = request.user.id
    if currentUserId == None : return False
    try:
        currentUser = User.objects.get(id = currentUserId)
        #change parameter below to check for different privilege
        if UserDetails.objects.get(user = currentUser).isEventManager:
            #logic starts
            return True
            #logic ends
    except ObjectDoesNotExist:
        return False


