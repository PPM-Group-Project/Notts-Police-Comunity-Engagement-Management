from django.urls import path

from . import views as ManagementView

urlpatterns = [
    path('', ManagementView.dashboard),
    path('login/', ManagementView.loginUser),
    path('logout/', ManagementView.logoutUser),
    path('officers/', ManagementView.officers),
    path('officers/add', ManagementView.addOfficer),
    path('officers/remove/<int:officerId>',ManagementView.removeOfficer),
    path('departments/', ManagementView.departments),
    path('departments/add', ManagementView.addDepartment),
    path('departments/remove/<int:departmentId>',ManagementView.removeDepartment),
    path('charts/officersPerDepartment',ManagementView.chartData_OfficersPerDepartment),
    path('nonauthorised/', ManagementView.notAuthorisedPage),
]
