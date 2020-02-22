from django.urls import path

from . import views

urlpatterns = [
    path('communities/', views.communities),
    path('communities/add',views.addCommunity),
    path('events/',views.events),
    path('events/scheduled',views.scheduledEvents),
    path('events/schedule/<int:eventid>',views.scheduleEvent)
]
