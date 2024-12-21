from django import forms
from django.contrib.auth.models import User
from accounts.models import ServiceModel, ServiceRequest


class ServiceModelForm(forms.ModelForm):
    class Meta:
        model = ServiceModel
        fields = ['name', 'description', 'price', 'category', 'duration', 'is_active']

        widgets = {
            'category': forms.Select(),
        }