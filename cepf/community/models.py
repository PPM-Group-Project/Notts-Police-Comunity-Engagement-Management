from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

class Representative(models.Model):
    """
    Databasase model for storing community representative details

    Future upgrades to the program include providing ability for 
    community respresentatives to login to a system and create 
    request for session
    """
    ## Unique Id for data entry in this model
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=100, null=False)
    lastName = models.CharField(max_length=100, null=False)
    eMail = models.EmailField(null=False)
    address = models.TextField()


class Community(models.Model):
    """
    Database model for storing communities on the system.

    Provides details about community, and also stores
    preffered frequency of officer visit sessions

    """
    ## Unique Id for data entry in this model
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    address = models.TextField()
    frequency = models.PositiveIntegerField(default=0, null=False)
    engagementStart = models.DateField(null=False)
    engagementStop = models.DateField(null=False)
    representative = models.ForeignKey(
        Representative, on_delete=models.SET_NULL, null=True
    )



class EventToSchedule(models.Model):
    """
     Database model for storing events that need to be scheduled.

     Events to be scheduled are added to this model automatically by
     calculating recommended date obtained to community model.
     NOTE: THESE ARE NOT SCHEDULED EVENTS!
     Each event needs manual review by Events Managers, after review,
     evented is added to ScheduledEvent models, and deleted from this one.
    """

    ## Unique Id for data entry in this model
    id = models.AutoField(primary_key=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    isManualyAdded = models.BooleanField(default=False)
    recommendedReview = models.BooleanField(default=False)
    canceledBefore = models.BooleanField(default=False)
    recommendedDate = models.DateField()
    recommendedTime = models.TimeField(default=None, null=True)

    def isOverdue(self):
        if self.recommendedTime:
            return (
                datetime.now().date() > self.recommendedDate
                and datetime.now().time() > self.recommendedTime
            )
        else:
            return datetime.now().date() > self.recommendedDate



class ScheduledEvent(models.Model):
    """
     Database model for storing events that are scheduled by Event Managers.

     When sucesfull, events get delted from this model and pushed to
     CompletedEvents model, where officer can leave a review.
     Also, officer can propose change to scheduled events, which must be approved
     by event managers
    """

    def reschedule(self):
        newEvent = EventToSchedule()
        newEvent.community = self.community
        newEvent.canceledBefore = True
        newEvent.recommendedDate = self.date
        newEvent.recommendedTime = self.time
        newEvent.save()
        self.delete()

    def complete(self):
        if True:
            event = CompletedEvent()
            event.id = self.id
            event.community = self.community
            event.date = self.date
            event.time = self.time
            event.save()
            for o in self.officers.all():
                event.officers.add(o)
            event.save()
            self.delete()
        else:
            pass
    ## Unique Id for data entry in this model
    id = models.AutoField(primary_key=True)
    officers = models.ManyToManyField(User)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()


class CompletedEvent(models.Model):
    """
    Database model for storing events that officers marked as complete

    This model will provide perament storage for all events on system, also
    will serve as a foreign key to feedback model contatining officer given
    feedback on efficiency of event
    """
    id = models.IntegerField(primary_key=True, null=False)
    officers = models.ManyToManyField(User)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
