from django.shortcuts import render, redirect, loader
from django.http import HttpResponse




def login(request):
    template = loader.get_template('login.html')
    context = {} 
    return HttpResponse(template.render(context,request))

def dashboard(request):
    #template = loader.get_template('departments.html')
    #context = {} 
    #return HttpResponse(template.render(context,request))
    return HttpResponse("Not implemented yet")

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