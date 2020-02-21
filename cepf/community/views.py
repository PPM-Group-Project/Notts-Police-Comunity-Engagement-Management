from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import loader
from django.http import HttpResponse
from datetime import datetime
from dateutil.relativedelta import relativedelta

from management.views import notAuthorisedPage
from management.views import isUserCommunityManager
from management.views import isUserEventManager
from management.views import getAuthsForUser

from management.models import UserDetails, Department
from .models import Representative, Community, EventToSchedule, ScheduledEvent


def communities(request):
    if isUserCommunityManager(request) == False:
        return redirect(notAuthorisedPage)
    template = loader.get_template("communities.html")
    context = {}
    context["permissions"] = getAuthsForUser(request)
    context["community"] = Community.objects.all()
    return HttpResponse(template.render(context, request))


def addCommunity(request):
    if isUserCommunityManager(request) == False:
        return redirect(notAuthorisedPage)
    if request.method == "POST":
        if True:
            com = Community()
            rep = Representative()
            com.name = request.POST.get("communityName")
            com.description = request.POST.get("communityDescription")
            com.address = request.POST.get("communityAddress")
            com.frequency = request.POST.get("communityFrequency")
            engagementStartDate = request.POST.get("communityStart")
            com.engagementStart = datetime.strptime( engagementStartDate, "%Y-%m-%d" ).date()

            engagementStopDate = request.POST.get("communityStop")
            com.engagementStop = datetime.strptime( engagementStopDate, "%Y-%m-%d" ).date()

            rep.firstName = request.POST.get("communityRepresentativeFirstName")
            rep.lastName = request.POST.get("communityRepresentativeLastName")
            rep.eMail = request.POST.get("communityRepresentativeEMail")
            rep.address = request.POST.get("communityRepresentativeAddress")
            com.representative = rep
            rep.save()
            com.save()

            # Calculate suggested events and put them in database
            if int(com.frequency) == 12:
                dates = []
                dates.append(com.engagementStart)
                mon_rel = relativedelta(months=1)
                while dates[-1] < com.engagementStop:
                    dates.append(dates[-1] + mon_rel)

                for i in dates:
                    event = EventToSchedule()
                    event.community = com
                    event.recommendedDate = i
                    event.save()

            elif int(com.frequency) == 4:
                dates = []
                dates.append(com.engagementStart)
                mon_rel = relativedelta(months=3)
                while dates[-1] < com.engagementStop:
                    dates.append(dates[-1] + mon_rel)

                for i in dates:
                    event = EventToSchedule()
                    event.community = com
                    event.recommendedDate = i
                    event.save()

            elif int(com.frequency) == 2:
                dates = []
                dates.append(com.engagementStart)
                mon_rel = relativedelta(months=6)
                while dates[-1] < com.engagementStop:
                    dates.append(dates[-1] + mon_rel)

                for i in dates:
                    event = EventToSchedule()
                    event.community = com
                    event.recommendedDate = i
                    event.save()

            elif int(com.frequency) == 1:
                dates = []
                dates.append(com.engagementStart)
                mon_rel = relativedelta(months=12)
                while dates[-1] < com.engagementStop:
                    dates.append(dates[-1] + mon_rel)

                for i in dates:
                    event = EventToSchedule()
                    event.community = com
                    event.recommendedDate = i
                    event.save()
            else:
                pass
    return redirect(communities)

def events(request):
    if isUserEventManager(request) == False:
        return redirect(notAuthorisedPage)
    template = loader.get_template("events.html")
    context = {}
    context["permissions"] = getAuthsForUser(request)
    context["event"] = EventToSchedule.objects.all().order_by('recommendedDate')
    context["officers"] = UserDetails.objects.exclude(user = 1)
    return HttpResponse(template.render(context, request))
