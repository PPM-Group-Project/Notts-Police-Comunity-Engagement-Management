from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import loader
from django.http import HttpResponse
from datetime import datetime


from management.views import notAuthorisedPage 
from management.views import isUserCommunityManager
from management.views import isUserEventManager 
from management.views import getAuthsForUser

from management.models import UserDetails,Department
from .models import Representative, Community


def communities(request):
    if isUserCommunityManager(request) == False:
        return redirect(notAuthorisedPage)
    template = loader.get_template('communities.html')
    context = {}
    context["permissions"] = getAuthsForUser(request)
    context["community"] = Community.objects.all()
    return HttpResponse(template.render(context, request))


def addCommunity(request):
    if isUserCommunityManager(request) == False:
        return redirect(notAuthorisedPage)
    if request.method == 'POST':
        try:
            com = Community()
            rep = Representative()
            com.name = request.POST.get('communityName')
            com.description = request.POST.get('communityDescription')
            com.address = request.POST.get('communityAddress')
            com.frequency = request.POST.get('communityFrequency')
            date =  request.POST.get('communityStart')
            date = date.replace("-","/")
            com.engagementStart = datetime.strptime(date, '%Y/%m/%d')
            rep.firstName = request.POST.get('communityRepresentativeFirstName')
            rep.lastName = request.POST.get('communityRepresentativeLastName')
            rep.eMail = request.POST.get('communityRepresentativeEMail')
            rep.address = request.POST.get('communityRepresentativeAddress')
            com.representative = rep
            com.save()
            rep.save()
        except:
            pass
    return redirect(communities)
