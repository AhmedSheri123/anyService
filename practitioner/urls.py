from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='practitioner_index'),
    path('plans', views.plans, name='plans'),
    path('MyService', views.MyService, name='MyService'),
    path('AddService', views.AddService, name='AddService'),
    path('EditService/<int:service_id>', views.EditService, name='EditService'),
    path('DeleteService/<int:service_id>', views.DeleteService, name='DeleteService'),
    path('MyServiceRequest', views.MyServiceRequest, name='MyServiceRequest'),
    path('RejectServiceRequest/<int:ser_req_id>', views.RejectServiceRequest, name='RejectServiceRequest'),
    path('AcceptServiceRequest/<int:ser_req_id>', views.AcceptServiceRequest, name='AcceptServiceRequest'),
    path('Profile', views.Profile, name='Profile'),
    path('ViewProfile/<int:user_id>', views.ViewProfile, name='PVProfile'),


]
