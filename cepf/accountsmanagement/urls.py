from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login),
    path('dashboard/', views.dashboard ),
    path('dashboard/officers/', views.officers),
    path('dashboard/departments/', views.departments),
    path('dashboard/communities',views.communities),

    
]