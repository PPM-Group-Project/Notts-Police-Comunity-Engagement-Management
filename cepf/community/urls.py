from django.urls import path

from . import views

urlpatterns = [
    path('add',views.addCommunity),
    path('', views.communities),
]
