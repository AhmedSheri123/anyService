from django.contrib import admin
from .models import ServiceCategory, ServiceRequest, ServiceModel, UserProfile, Review
# Register your models here.
admin.site.register(ServiceCategory)
admin.site.register(ServiceRequest)
admin.site.register(ServiceModel)
admin.site.register(UserProfile)
admin.site.register(Review)