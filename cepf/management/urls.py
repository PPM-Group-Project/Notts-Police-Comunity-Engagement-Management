from django.urls import path

import views

urlpatterns = [
    path('', views.dashboard ),
    path('login/', views.loginUser),
    path('logout/', views.logoutUser),
    path('nonauthorised/',views.notAuthorisedPage),
    path('officers/', views.officers),
    path('departments/', views.departments),

]