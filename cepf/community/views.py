#from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import loader
from django.http import HttpResponse
#from django.contrib.auth.forms import UserCreationForm
from management.views import notAuthorisedPage, isUserDepartmentManager, getAuthsForUser
# Create your views here.


def communities(request):
    if isUserDepartmentManager(request) == False:
        return redirect(notAuthorisedPage)
    template = loader.get_template('communities.html')
    context = {}
    context["permissions"] = getAuthsForUser(request)
    return HttpResponse(template.render(context, request))


def addCommunity(request):
    pass
