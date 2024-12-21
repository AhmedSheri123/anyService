from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, PractitionerProfileModel


class PractitionerSignUpModelForm(forms.ModelForm):
    password = forms.CharField(label='password', max_length=254, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'اسمك...'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'الكنية...'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'name@example.com'})
        }

class ProfilePractitionerUserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'اسمك...'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'الكنية...'}),
        }

class PractitionerUserProfileSignUpModelForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender', 'phone_number', 'city', 'address', 'birthdate']

        widgets = {
            'gender': forms.Select(attrs={'class':'form-control', 'placeholder':'الجنس'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control', 'placeholder':'رقم الجوال'}),
            'city': forms.Select(attrs={'class':'form-control', 'placeholder':'المدينة'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'عنوان'}),
            'birthdate': forms.DateInput(attrs={'class':'form-control', 'placeholder':'تاريخ الميلاد', 'type':'date'}),
        }

class PractitionerProfileSignUpModelForm(forms.ModelForm):
    class Meta:
        model = PractitionerProfileModel
        fields = ['specialty', 'specialty_years_of_experience', 'description']

        widgets = {
            'specialty': forms.TextInput(attrs={'class':'form-control', 'placeholder':'سباك، كهربائي، الخ'}),
            'specialty_years_of_experience': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'سنوات الخبرة للتخصص'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'نبذ مختصرة عنك'}),
        }

class LoginForm(forms.Form):
    email = forms.EmailField(label='email', max_length=254, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'name@example.com'}))
    password = forms.CharField(label='password', max_length=254, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
