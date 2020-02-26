from django.shortcuts import redirect
from django.shortcuts import loader
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ObjectDoesNotExist

from .models import UserDetails, Department
from django.contrib.auth.models import User

def notAuthorisedPage(request):
    return HttpResponse("You are not authorised to access this property!")

def loginUser(request):
    template = loader.get_template('login.html')
    context = {}

    if (request.user.is_authenticated):
        return redirect(dashboard)

    if request.method == 'GET':
        return HttpResponse(template.render(context, request))
    else:
        try:
            username = request.POST.get('username')
            passwd = request.POST.get('password')
            user = authenticate(username=username, password=passwd)
            login(request, user)
            return redirect(dashboard)
        except AttributeError:
            context["invalidLogin"] = True
            return HttpResponse(template.render(context, request))

def logoutUser(request):
    logout(request)
    return redirect(loginUser)

def dashboard(request):
    template = loader.get_template('personalDetails.html')
    context = {}
    if (request.user.is_authenticated == False):
        return redirect(loginUser)
    context["permissions"] = getAuthsForUser(request)
    return HttpResponse(template.render(context, request))

def officers(request):
    if isUserOfficerManager(request) == False:
        return redirect(notAuthorisedPage)
    template = loader.get_template('officers.html')
    listOfDepartments = Department.objects.all()
    context = {}
    context["permissions"] = getAuthsForUser(request)
    context["departments"] = listOfDepartments
    message = request.GET.get('tableSearch')
    if message:
        user = User.objects.filter(username__contains = message)
        if user:
            listOfOfficers = UserDetails.objects.filter()
            context["officers"] = listOfOfficers
    else:
        listOfOfficers = UserDetails.objects.exclude(user = 1)
        context["officers"] = listOfOfficers

    return HttpResponse(template.render(context, request))

def addOfficer(request):
    if isUserOfficerManager(request) == False:
        return redirect(notAuthorisedPage)
    if request.method == 'POST':
        try:
            user = User()
            user.first_name = request.POST.get('officerName')
            user.last_name = request.POST.get('officerSurname')
            user.email = request.POST.get('officereMail')
            user.username = user.email.split('@')[0]
            user.set_password("default")
            details = UserDetails()
            details.user = user
            details.badgeNumber = request.POST.get('officerBadgeNumber')
            details.department = Department.objects.get(id=request.POST.get('department'))
            user.save()
            details.save()
        except:
            return redirect(officers(request))
    return redirect(officers)

def removeOfficer(request,officerId):
    if isUserOfficerManager(request) == False:
        return redirect(notAuthorisedPage)
    User.objects.get(id = officerId).delete()
    return redirect(officers)

def departments(request):
    if isUserOfficerManager(request) == False:
        return redirect(notAuthorisedPage)
    template = loader.get_template('departments.html')
    context = {}
    context["permissions"] = getAuthsForUser(request)
    context["officers"] = UserDetails.objects.all()
    context["departments"] = Department.objects.filter().exclude(id = 1)
    for dep in context["departments"]:
        x = Department.objects.get(id=dep.id)
        dep.count = UserDetails.objects.filter(department=x).count()
    return HttpResponse(template.render(context, request))

def addDepartment(request):
    if isUserDepartmentManager(request) == False:
        return redirect(notAuthorisedPage)
    if request.method == 'POST':
        try:
            dep = Department()
            dep.departmentName = request.POST.get('departmentName')
            dep.responsibleOfficer = User.objects.get(
                id=request.POST.get('officerInCharge'))
            dep.departmentDescription = request.POST.get(
                'departmentDescription')
            if request.POST.get('isOfficerManager'):
                dep.isOfficerManager = True
            if request.POST.get('isDepartmentManager'):
                dep.isDepartmentManager = True
            if request.POST.get('isCommunityManager'):
                dep.isCommunityManager = True
            if request.POST.get('isEventManager'):
                dep.isEventManager = True
            dep.save()
        except:
            return redirect(departments)
    return redirect(departments)

def removeDepartment(request,departmentId):
    if isUserDepartmentManager(request) == False:
        return redirect(notAuthorisedPage)
    Department.objects.get(id = departmentId).delete()
    return redirect(departments)

def isUserOfficerManager(request):
    currentUser = returnCurrentUser(request)
    # change parameter below to check for different privilege
    if UserDetails.objects.get(user=currentUser).isOfficerManager():
        return True
    return False

def isUserDepartmentManager(request):
    currentUser = returnCurrentUser(request)
    # change parameter below to check for different privilege
    if UserDetails.objects.get(user=currentUser).isDepartmentManager():
        return True
    return False
def isUserEventManager(request):
    currentUser = returnCurrentUser(request)
    # change parameter below to check for different privilege
    if UserDetails.objects.get(user=currentUser).isEventManager():
        return True
    return False

def isUserCommunityManager(request):
    currentUser = returnCurrentUser(request)
    # change parameter below to check for different privilege
    if UserDetails.objects.get(user=currentUser).isCommunityManager():
        return True
    return False

def returnCurrentUser(details):
    currentUserId = details.user.id
    if currentUserId == None:
        return redirect(notAuthorisedPage)
    try:
        currentUser = User.objects.get(id=currentUserId)
        return currentUser
    except ObjectDoesNotExist:
        return redirect(notAuthorisedPage)

def getAuthsForUser(details):
    auths = {}
    auths["isOfficerManager"] = isUserOfficerManager(details)
    auths["isDepartmentManager"] = isUserDepartmentManager(details)
    auths["isEventManager"] = isUserEventManager(details)
    auths["isCommunityManager"] = isUserCommunityManager(details)
    return auths
