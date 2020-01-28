from django.shortcuts import render, redirect, loader
from django.http import HttpResponse

# Create your views here.

def events(request):
    template = loader.get_template('events.html')
    context = {} #no data to put on front page
    return HttpResponse(template.render(context,request))