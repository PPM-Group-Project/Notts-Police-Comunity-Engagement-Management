#from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import loader
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
#from django.contrib.auth.forms import UserCreationForm

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
            email = request.POST.get('email')
            passwd = request.POST.get('password')
            user = authenticate(username = email, password = passwd)
            print(user)
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
    currentUserId = request.user.id
    if currentUserId == None : return redirect(notAuthorisedPage)
    template = loader.get_template('officers.html')
    context = {} 
    return HttpResponse(template.render(context,request))

def addOfficer(request):
    pass

def departments(request):
    currentUserId = request.user.id
    if currentUserId == None : return redirect(notAuthorisedPage)
    template = loader.get_template('departments.html')
    context = {} 
    return HttpResponse(template.render(context,request))

def addDepartment(request):
    pass
