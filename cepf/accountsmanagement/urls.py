from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login),
    path('dashboard/', views.users),
    path('dashboard/officers/', views.users),

    
]