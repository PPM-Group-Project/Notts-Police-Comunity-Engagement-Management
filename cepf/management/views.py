from django.shortcuts import render, redirect, loader
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm





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
        except:
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

def departments(request):
    template = loader.get_template('departments.html')
    context = {} 
    return HttpResponse(template.render(context,request))

def officers(request):
    template = loader.get_template('officers.html')
    context = {} 
    return HttpResponse(template.render(context,request))

def communities(request):
    template = loader.get_template('communities.html')
    context = {}
    return HttpResponse(template.render(context,request))