from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard),
    path('login/', views.loginUser),
    path('logout/', views.logoutUser),
    path('nonauthorised/', views.notAuthorisedPage),
    path('officers/', views.officers),
    path('officers/add', views.addOfficer),
    path('departments/', views.departments),
    path('departments/add', views.addDepartment),
]
