from django.urls import path
from . import views

urlpatterns = [
    path('redirect_index', views.redirect_index, name='redirect_index'),
    path('PractitionerSignup', views.PractitionerSignup, name='PractitionerSignup'),
    path('PractitionerLogin', views.PractitionerLogin, name='PractitionerLogin'),
    path('PractitionerLogout', views.PractitionerLogout, name='PractitionerLogout'),

    path('CustomerSignup', views.CustomerSignup, name='CustomerSignup'),
    path('CustomerLogin', views.CustomerLogin, name='CustomerLogin'),
    path('CustomerLogout', views.CustomerLogout, name='CustomerLogout'),
]
