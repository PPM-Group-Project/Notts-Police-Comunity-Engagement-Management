from django.urls import path

from . import views

urlpatterns = [
    path('communities/', views.communities),
    path('communities/add',views.addCommunity),
    path('communities/remove/<communityId>',views.removeCommunity),
    path('events/',views.events),
    path('events/scheduled/',views.scheduledEvents),
    path('events/schedule/<int:eventid>',views.scheduleEvent),
    path('events/reschedule/<int:eventid>',views.rescheduleEvent),
    path('events/completed/',views.completedEvents),
    path('myevents/',views.myEvents),
    path('myevents/completed/',views.myEventsCompleted),
    path('myevents/complete/<int:eventid>',views.completeEvent),

]
