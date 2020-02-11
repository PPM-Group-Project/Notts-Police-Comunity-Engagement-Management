#from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import loader
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
#from django.contrib.auth.forms import UserCreationForm
from management.views import notAuthorisedPage
from django.contrib.auth.models import User
# Create your views here.


def communities(request):
    currentUserId = request.user.id
    if currentUserId == None : return redirect(notAuthorisedPage)
    currentUser = User.objects.get(id = currentUserId)
    template = loader.get_template('communities.html')
    context = {}
    return HttpResponse(template.render(context,request))

def addCommunity(request):
    pass