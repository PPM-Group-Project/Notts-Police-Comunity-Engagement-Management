from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import loader
from django.http import HttpResponse
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

from management.views import notAuthorisedPage
from management.views import isUserCommunityManager
from management.views import isUserEventManager
from management.views import getAuthsForUser
from management.views import returnCurrentUser

from django.contrib.auth.models import User
from management.models import UserDetails, Department
from .models import *

def chartData_FinishedEventsPerCommunity(request):
    backgroundColor = ['#FF7F50','#FF6347','#FF4500','#FFD700','#FFA500','#FF8C00','#003f5c','#2f4b7c','#665191','#a05195','#d45087','#f95d6a','#ff7c43','#ffa600']
    labels = []
    data = []
    colour = []
    for c in Community.objects.all():
        count = CompletedEvent.objects.filter(community = c).count()
        if (count == 0): continue
        name = c.name
        labels.append(name)
        data.append(count)
        colour.append(backgroundColor.pop())
    
    finalObj = {}
    finalObj["labels"] = labels
    finalObj["datasets"] = [{"data":data, "backgroundColor" : colour}]
    return HttpResponse(json.dumps(finalObj), content_type="application/json")

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
        com = Community()
        rep = Representative()
        try:
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
        except:
            rep.delete()
            com.delete()
            event.delete()
    return redirect(communities)

def removeCommunity(request,communityId):
    if isUserCommunityManager(request) == False:
        return redirect(notAuthorisedPage)
    Community.objects.get(id = communityId).delete()
    return redirect(communities)

def events(request):
    if isUserEventManager(request) == False:
        return redirect(notAuthorisedPage)
    template = loader.get_template("events.html")
    context = {}
    context["permissions"] = getAuthsForUser(request)
    context["events"] = EventToSchedule.objects.all().order_by('recommendedDate','recommendedTime')
    context["officers"] = UserDetails.objects.exclude(user = 1)
    return HttpResponse(template.render(context, request))

def scheduledEvents(request):
    if isUserEventManager(request) == False:
        return redirect(notAuthorisedPage)
    template = loader.get_template("scheduledevents.html")
    context = {}
    context["permissions"] = getAuthsForUser(request)
    context["events"] = ScheduledEvent.objects.all().order_by('date' , 'time')
    return HttpResponse(template.render(context, request))

def scheduleEvent(request,eventid):
    if isUserEventManager(request) == False:
        return redirect(notAuthorisedPage)
    if request.method == 'POST':
        newEvent = ScheduledEvent()
        try:
            officers = request.POST.getlist("officers")
            eventdatetime = request.POST.get("datetime")
            eventdatetime = datetime.strptime( eventdatetime, "%Y-%m-%dT%H:%M")
            eventSchedule = EventToSchedule.objects.get(id = eventid)
            newEvent.community = eventSchedule.community
            newEvent.date = eventdatetime.date()
            newEvent.time = eventdatetime.time()
            newEvent.save()
            for officer in officers:
                newEvent.officers.add(User.objects.get(id = int(officer)))
            newEvent.save()
            eventSchedule.delete()
        except:
            newEvent.delete()
        return redirect(scheduledEvents)

def rescheduleEvent(request,eventid):
    if isUserEventManager(request) == False:
        return redirect(notAuthorisedPage)
    event = ScheduledEvent.objects.get(id = eventid).reschedule()
    return redirect(events)

def completedEvents(request):
    if isUserEventManager(request) == False:
        return redirect(notAuthorisedPage)
    template = loader.get_template("completedevents.html")
    context = {}
    context["permissions"] = getAuthsForUser(request)
    context["events"] =  CompletedEvent.objects.all().order_by('date' , 'time')
    return HttpResponse(template.render(context, request))

def completeEvent(request,eventid):
    #beware; this view does not need authentication, every user can access it
    currentUser = returnCurrentUser(request) 
    if currentUser == None : return redirect(notAuthorisedPage)
    ScheduledEvent.objects.get(id = eventid).complete()
    return redirect(myEvents)

def myEvents(request):
    #beware; this view does not need authentication, every user can access it
    currentUser = returnCurrentUser(request) 
    if currentUser == None : return redirect(notAuthorisedPage)
    template = loader.get_template("myevents.html")
    context = {}
    context["permissions"] = getAuthsForUser(request)
    context["events"] = ScheduledEvent.objects.filter(officers__id = currentUser.id).distinct()
    return HttpResponse(template.render(context,request))

def myEventsCompleted(request):
    #beware; this view does not need authentication, every user can access it
    currentUser = returnCurrentUser(request) 
    if currentUser == None : return redirect(notAuthorisedPage)
    template = loader.get_template("mycompletedevents.html")
    context = {}
    context["permissions"] = getAuthsForUser(request)
    context["events"] = CompletedEvent.objects.filter(officers__id = currentUser.id).distinct()
    return HttpResponse(template.render(context,request))
    