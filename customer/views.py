from django.shortcuts import render, redirect
from accounts.models import ServiceCategory, ServiceModel, ServiceRequest, Review
from django.contrib import messages
from accounts.forms import ProfilePractitionerUserModelForm, PractitionerUserProfileSignUpModelForm
from .libs import haversine
# Create your views here.


def get_nearby_places_haversine(user_lat, user_lng, max_distance_km):
    places = ServiceModel.objects.filter()
    nearby_places = []

    for place in places:
        if user_lat and user_lng:
            distance = haversine(user_lat, user_lng, place.geo_lat, place.geo_lng)
            if distance <= max_distance_km:
                nearby_places.append((place, round(distance, 2)))
        else:
            nearby_places.append((place, None))
    # ترتيب النتائج حسب المسافة
    nearby_places.sort(key=lambda x: x[1])
    return nearby_places


def index(request):
    return render(request, 'customer/index.html')

def Categorys(request):
    categorys = ServiceCategory.objects.filter()

    return render(request, 'customer/services/service_category.html', {'categorys':categorys})

def Services(request, category_id):
    category = ServiceCategory.objects.get(id=category_id)
    services = ServiceModel.objects.filter(category=category)
    user_lat = request.GET.get('lat')
    user_lng = request.GET.get('lng')
    
    services = get_nearby_places_haversine(user_lat, user_lng, 10)
    return render(request, 'customer/services/services.html', {'services':services, 'category':category, 'user_lat':user_lat, 'user_lng':user_lng})

def Service(request, service_id):
    service = ServiceModel.objects.get(id=service_id)
    reviews = Review.objects.filter(service_request__service=service)
    return render(request, 'customer/services/service.html', {'service':service, 'reviews':reviews})

def MyServiceRequest(request):
    customer = request.user
    customer_profile = customer.userprofile

    ser_reqs = ServiceRequest.objects.filter(customer=customer_profile)
    return render(request, 'customer/service_requests/my_service_requests.html', {'ser_reqs':ser_reqs})

def CustomerRequestService(request, service_id):
    customer = request.user
    customer_profile = customer.userprofile
    service = ServiceModel.objects.get(id=service_id)
    if customer != service.provider:
        ser_req = ServiceRequest.objects.create(customer=customer_profile, service=service)
        ser_req.save()
        messages.success(request, 'تم طلب الخدمة بنجاح, الرجاء الانتظار حتى يتم الموافقة على طلبك من قبل صاحب الخدمة لبدء المحادثة')
        return redirect('CustomerServiceRequest')
    else:
        messages.error(request, 'لا يمكن لصالحب الخدمة طلب الخدمة')
        return redirect('Service', service_id)

def CanselServiceRequest(request, ser_req_id):
    ser_req = ServiceRequest.objects.get(id=ser_req_id)
    ser_req.delete()
    return redirect('CustomerServiceRequest')


def Profile(request):
    provider = request.user
    provider_userprofile = provider.userprofile

    user_form = ProfilePractitionerUserModelForm(instance=provider)
    userprofile_form = PractitionerUserProfileSignUpModelForm(instance=provider_userprofile)

    if request.method == 'POST':
        user_form = ProfilePractitionerUserModelForm(data=request.POST, instance=provider)
        userprofile_form = PractitionerUserProfileSignUpModelForm(data=request.POST, instance=provider_userprofile)
        if user_form.is_valid() and userprofile_form.is_valid():
            profile_img_base64 = request.POST.get('profile_img', '')
            if profile_img_base64 == 'data:,': profile_img_base64 = ''

            user_form.save()
            provider_userprofile = userprofile_form.save(commit=False)
            provider_userprofile.profile_img_base64 = profile_img_base64
            provider_userprofile.save()

            messages.success(request, 'تم تعديل الحساب بنجاح')
            # return redirect('PractitionerLogin')
        else:messages.error(request, f"{user_form.errors}{userprofile_form.errors}")
        
    return render(request, 'accounts/customer/profile/EditProfile.html', {'user_form':user_form, 'userprofile_form':userprofile_form, 'provider_userprofile':provider_userprofile})


def ReviewRequestService(request, ser_req_id):
    reviewer = request.user
    reviewer_userprofile = reviewer.userprofile
    ser_req = ServiceRequest.objects.get(id=ser_req_id)

    if request.method == 'POST':
        rating = request.POST.get('rate', '0')
        comment = request.POST.get('comment', '')
        review = Review.objects.create(service_request=ser_req, reviewer=reviewer_userprofile, rating=rating, comment=comment)
        review.save()
    return redirect('CustomerServiceRequest')

def set_geo_location_redir_to_categorys(request, category_id):
    
    return render(request, 'customer/set_geo_location.html', {'category_id':category_id})