from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import PractitionerSignUpModelForm, PractitionerProfileSignUpModelForm, PractitionerUserProfileSignUpModelForm, LoginForm
from .libs import RandomDigitsGen
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
# Create your views here.

def redirect_index(request):
    user = request.user
    if user.is_authenticated:
        userprofile = user.userprofile
        if userprofile.profile_type == '3':
            return redirect('MyService')
        else:
            return redirect('Categorys')

def PractitionerSignup(request):
    user_form = PractitionerSignUpModelForm()
    userprofile_form = PractitionerUserProfileSignUpModelForm()
    practitioner_userprofile_form = PractitionerProfileSignUpModelForm()

    if request.method == 'POST':
        user_form = PractitionerSignUpModelForm(data=request.POST)
        userprofile_form = PractitionerUserProfileSignUpModelForm(data=request.POST)
        practitioner_userprofile_form = PractitionerProfileSignUpModelForm(data=request.POST)
        if user_form.is_valid() and userprofile_form.is_valid() and practitioner_userprofile_form.is_valid():
            password = user_form.cleaned_data.get('password')

            user = user_form.save(commit=False)
            user.username = RandomDigitsGen()
            user.set_password(password)
            practitioner_profile = practitioner_userprofile_form.save()
            userprofile = userprofile_form.save(commit=False)
            userprofile.user = user
            userprofile.practitioner_profile = practitioner_profile
            userprofile.profile_type = '3'

            user.save()
            userprofile.save()
            messages.success(request, 'تم انشاء الحساب بنجاح')
            return redirect('PractitionerLogin')
        else:messages.error(request, f"{user_form.errors}{userprofile_form.errors}{practitioner_userprofile_form.errors}")
        # else:print()
    return render(request, 'accounts/practitioner/signup.html', {'user_form':user_form, "userprofile_form":userprofile_form, 'practitioner_userprofile_form':practitioner_userprofile_form})



def PractitionerLogin(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            users = User.objects.filter(email=email)
            if users.exists():
                user = users.first()
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'تم التسجيل بنجاح')
                    return redirect('redirect_index')
                else:messages.error(request, 'بريد الالكتروني او كلمة المرور خاطئ')
            else:messages.error(request, 'بريد الالكتروني او كلمة المرور خاطئ')
        else:messages.error(request, form.errors)
    return render(request, 'accounts/practitioner/login.html', {'form':form})





def CustomerSignup(request):
    user_form = PractitionerSignUpModelForm()
    userprofile_form = PractitionerUserProfileSignUpModelForm()

    if request.method == 'POST':
        user_form = PractitionerSignUpModelForm(data=request.POST)
        userprofile_form = PractitionerUserProfileSignUpModelForm(data=request.POST)
        if user_form.is_valid() and userprofile_form.is_valid():
            password = user_form.cleaned_data.get('password')

            user = user_form.save(commit=False)
            user.username = RandomDigitsGen()
            user.set_password(password)
            userprofile = userprofile_form.save(commit=False)
            userprofile.user = user
            userprofile.profile_type = '2'

            user.save()
            userprofile.save()
            messages.success(request, 'تم انشاء الحساب بنجاح')
            return redirect('PractitionerLogin')
        else:messages.error(request, f"{user_form.errors}{userprofile_form.errors}")
        # else:print()
    return render(request, 'accounts/customer/signup.html', {'user_form':user_form, "userprofile_form":userprofile_form})



def CustomerLogin(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            users = User.objects.filter(email=email)
            if users.exists():
                user = users.first()
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'تم التسجيل بنجاح')
                    return redirect('redirect_index')
                else:messages.error(request, 'بريد الالكتروني او كلمة المرور خاطئ')
            else:messages.error(request, 'بريد الالكتروني او كلمة المرور خاطئ')
        else:messages.error(request, form.errors)
    return render(request, 'accounts/customer/login.html', {'form':form})

def PractitionerLogout(request):
    logout(request)
    return redirect('PractitionerLogin')

def CustomerLogout(request):
    logout(request)
    return redirect('CustomerLogin')
