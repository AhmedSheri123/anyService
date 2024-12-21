from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='customer_index'),
    path('Categorys', views.Categorys, name='Categorys'),
    path('Services/<int:category_id>', views.Services, name='Services'),
    path('set_geo_location_redir_to_categorys/<int:category_id>', views.set_geo_location_redir_to_categorys, name='set_geo_location_redir_to_categorys'),
    path('Service/<int:service_id>', views.Service, name='Service'),
    path('MyServiceRequest', views.MyServiceRequest, name='CustomerServiceRequest'),
    path('CustomerRequestService/<int:service_id>', views.CustomerRequestService, name='CustomerRequestService'),
    path('CanselServiceRequest/<int:ser_req_id>', views.CanselServiceRequest, name='CanselServiceRequest'),
    path('ReviewRequestService/<int:ser_req_id>', views.ReviewRequestService, name='ReviewRequestService'),
    path('Profile', views.Profile, name='CustomerProfile'),
]
