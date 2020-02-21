from django.db import models

# Databasase model for storing community representative details,
# future upgrades to the program include providing ability for 
# community respresentatives to login to a system and create 
# request for session
class Representative(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=100, null=False)
    lastName = models.CharField(max_length=100, null=False)
    eMail = models.EmailField(null=False)
    address = models.TextField()

# Database model for storing communities on the system.
# Provides details about community, and also stores
# preffered frequency of officer visit sessions
class Community(models.Model):
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

# Database model for storing events that need to be scheduled.
# Events to be scheduled are added to this model automatically by
# calculating recommended date obtained to community model.
# NOTE: THESE ARE NOT SCHEDULED EVENTS!
# Each event needs manual review by Events Managers, after review,
# evented is added to ScheduledEvent models, and deleted from this one.
class EventToSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    isManualyAdded = models.BooleanField(default=False)
    recommendedReview = models.BooleanField(default=False)
    canceledBefore = models.BooleanField(default=False)
    recommendedDate = models.DateTimeField()

# Database model for storing events that are scheduled by Event Managers.
# When sucesfull, events get delted from this model and pushed to
# CompletedEvents model, where officer can leave a review.
# Also, officer can propose change to scheduled events, which must be approved
# by events managers
class ScheduledEvent(models.Model):
    id = models.AutoField(primary_key=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    date = models.DateTimeField()

