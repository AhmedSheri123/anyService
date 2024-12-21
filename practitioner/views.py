from django.shortcuts import render, redirect
from adminDashboard.models import SubscriptionsModel
from accounts.models import ServiceModel, ServiceRequest, Review
from .forms import ServiceModelForm
from django.contrib import messages
from accounts.forms import ProfilePractitionerUserModelForm, PractitionerProfileSignUpModelForm, PractitionerUserProfileSignUpModelForm
from messenger.models import MessagesModel, MessengerModel
from django.contrib.auth.models import User
# Create your views here.


def index(request):
    return render(request, 'practitioner/index.html')

def plans(request):
    subscriptions = SubscriptionsModel.objects.filter(is_enabled=True)
    return render(request, 'practitioner/plans.html', {'subscriptions':subscriptions})

def MyService(request):
    provider = request.user
    provider_userprofile = provider.userprofile

    services = ServiceModel.objects.filter(provider=provider)

    return render(request, 'practitioner/services/my_services.html', {'services':services})

def AddService(request):
    provider = request.user
    provider_userprofile = provider.userprofile
    
    
    if request.method == 'POST':
        form = ServiceModelForm(data=request.POST)
        if form.is_valid():
            profile_img_base64 = request.POST.get('profile_img', '')
            geo_lat = request.POST.get('lat', '')
            geo_lng = request.POST.get('lng', '')
 
            service = form.save(commit=False)
            service.provider = provider
            service.img_base64 = profile_img_base64
            service.geo_lat = geo_lat
            service.geo_lng = geo_lng
            service.save()
            messages.success(request, 'تم إضافة الخدمة بنجاح.')
            return redirect('MyService')
    else:form = ServiceModelForm()
    return render(request, 'practitioner/services/add_service.html', {'form':form})

def EditService(request, service_id):
    provider = request.user
    service = ServiceModel.objects.get(id=service_id)

    if request.method == 'POST':
        form = ServiceModelForm(data=request.POST, instance=service)
        if form.is_valid():
            profile_img_base64 = request.POST.get('profile_img', '')
            geo_lat = request.POST.get('lat', '')
            geo_lng = request.POST.get('lng', '')

            service = form.save(commit=False)
            service.img_base64 = profile_img_base64
            service.geo_lat = geo_lat
            service.geo_lng = geo_lng
            service.save()
            messages.success(request, 'تم تعديل الخدمة بنجاح.')
            return redirect('MyService')
    else:form = ServiceModelForm(instance=service)
    return render(request, 'practitioner/services/edit_service.html', {'form':form, 'service':service})


def DeleteService(request, service_id):
    service = ServiceModel.objects.get(id=service_id)
    service.delete()
    messages.success(request, 'تم حذف الخدمة بنجاح.')
    return redirect('MyService')


def MyServiceRequest(request):
    provider = request.user

    ser_reqs = ServiceRequest.objects.filter(service__provider=provider)
    return render(request, 'practitioner/service_requests/my_service_requests.html', {'ser_reqs':ser_reqs})

def Profile(request):
    provider = request.user
    provider_userprofile = provider.userprofile
    provider_profile = provider_userprofile.practitioner_profile

    user_form = ProfilePractitionerUserModelForm(instance=provider)
    userprofile_form = PractitionerUserProfileSignUpModelForm(instance=provider_userprofile)
    practitioner_userprofile_form = PractitionerProfileSignUpModelForm(instance=provider_profile)

    if request.method == 'POST':
        user_form = ProfilePractitionerUserModelForm(data=request.POST, instance=provider)
        userprofile_form = PractitionerUserProfileSignUpModelForm(data=request.POST, instance=provider_userprofile)
        practitioner_userprofile_form = PractitionerProfileSignUpModelForm(data=request.POST, instance=provider_profile)
        if user_form.is_valid() and userprofile_form.is_valid() and practitioner_userprofile_form.is_valid():
            profile_img_base64 = request.POST.get('profile_img', '')
            if profile_img_base64 == 'data:,': profile_img_base64 = ''

            user_form.save()
            provider_userprofile = userprofile_form.save(commit=False)
            provider_userprofile.profile_img_base64 = profile_img_base64
            provider_userprofile.save()

            practitioner_userprofile_form.save()
            messages.success(request, 'تم تعديل الحساب بنجاح')
            # return redirect('PractitionerLogin')
        else:messages.error(request, f"{user_form.errors}{userprofile_form.errors}{practitioner_userprofile_form.errors}")
        
    return render(request, 'accounts/practitioner/profile/EditProfile.html', {'user_form':user_form, 'userprofile_form':userprofile_form, 'practitioner_userprofile_form':practitioner_userprofile_form, 'provider_userprofile':provider_userprofile})


def ViewProfile(request, user_id):
    provider = User.objects.get(id=user_id)
    provider_userprofile = provider.userprofile
    provider_profile = provider_userprofile.practitioner_profile
    services = ServiceModel.objects.filter(provider=provider)
    reviews = Review.objects.filter(service_request__service__provider=provider)

    return render(request, 'accounts/practitioner/profile/ViewProfile.html', {'provider':provider, 'provider_userprofile':provider_userprofile, 'provider_profile':provider_profile, 'services':services, 'reviews':reviews})
                  
def RejectServiceRequest(request, ser_req_id):
    ser_req = ServiceRequest.objects.get(id=ser_req_id)
    ser_req.status = 'rejected'
    ser_req.save()
    messages.success(request, 'تم العملية بنجاح.')
    return redirect('MyServiceRequest')

def AcceptServiceRequest(request, ser_req_id):
    ser_req = ServiceRequest.objects.get(id=ser_req_id)
    ser_req.status = 'accepted'
    ser_req.save()
    messages.success(request, 'تم العملية بنجاح.')
    return redirect('MyServiceRequest')

