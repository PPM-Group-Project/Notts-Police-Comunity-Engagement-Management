from django.shortcuts import render, redirect, loader
from django.http import HttpResponse


def users(request):
    template = loader.get_template('officers.html')
    context = {} #no data to put on front page
    return HttpResponse(template.render(context,request))


def login(request):
    template = loader.get_template('login.html')
    context = {} #no data to put on front page
    return HttpResponse(template.render(context,request))