from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .choices import citys, GenderFields, PractitionerProfileStateFields
from .libs import when_published

# Create your models here.


profile_type_choices = (
    ('1', 'admin'),
    ('2', 'customer'),
    ('3', 'practitioner'),
)

service_request_status_choices = [('pending', 'في انتظار الموافقة'), ('accepted', 'تم القبول الطلب'), ('rejected', 'تم الرفض الطلب'), ('completed', 'الطلب مكتمل')]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_type = models.CharField(max_length=50, choices=profile_type_choices)
    profile_img_base64 = models.TextField()
    gender = models.CharField(max_length=100, choices=GenderFields, default='1')
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    city = models.CharField(max_length=100, choices=citys, null=True)
    address = models.CharField(max_length=255, null=True)
    birthdate = models.DateField(null=True)
    practitioner_profile = models.ForeignKey('PractitionerProfileModel', on_delete=models.CASCADE, null=True)

    geo_lat = models.CharField(max_length=254, blank=True, null=True)
    geo_lng = models.CharField(max_length=254 , blank=True, null=True)

    is_active = models.BooleanField(default=False)
    last_active_datetime = models.DateTimeField(null=True, blank=True)
    
    is_in_chat = models.BooleanField(default=False)
    active_messenger = models.ForeignKey('messenger.MessengerModel', on_delete=models.SET_NULL, null=True, blank=True)
    
    dont_receive_msg_from_companys = models.BooleanField(default=False)
    dont_receive_msg_from_employees = models.BooleanField(default=False)

    @property
    def get_full_name(self):
        full_name = f'{self.user.first_name} {self.user.last_name}'
        return full_name
    
    def __str__(self):
        return self.get_full_name + ' ' + self.user.username

class PractitionerProfileModel(models.Model):
    specialty = models.CharField(max_length=100)  # e.g., plumber, electrician, etc.
    specialty_years_of_experience = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    profile_state = models.CharField(max_length=200, choices=PractitionerProfileStateFields, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_splited_desc(self):
        return self.description.split('\n')
    
    def __str__(self):
        return f"{self.specialty}"

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ServiceModel(models.Model):
    # حقل لاسم الخدمة، مثل "تصليح كهربائي"
    name = models.CharField(max_length=100, help_text="اسم الخدمة التي يقدمها صاحب المهنة.", verbose_name="اسم الخدمة")

    # وصف مفصل للخدمة لتعريف العميل بها
    description = models.TextField(help_text="وصف شامل للخدمة يوضح تفاصيلها وما تقدمه.", verbose_name="وصف الخدمة")

    img_base64 = models.TextField(null=True)
    
    # السعر المبدئي أو تكلفة الخدمة
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="سعر الخدمة أو التكلفة المبدئية لها.", verbose_name="السعر")

    # الفئة التي تنتمي إليها الخدمة (مثلاً: كهرباء، سباكة، نجارة)
    category = models.ForeignKey(ServiceCategory, help_text="الفئة العامة التي تندرج تحتها الخدمة.", verbose_name="الفئة", null=True, on_delete=models.CASCADE)

    #حقل يمكن أن يوضح الوقت المتوقع لإكمال الخدمة.
    duration = models.CharField(max_length=50, help_text="المدة الزمنية المتوقع لإكمال الخدمة.", null=True, verbose_name="المدة المتوقعة")

    # تحديد ما إذا كانت الخدمة متاحة حاليًا أم لا
    is_active = models.BooleanField(default=True, help_text="حالة الخدمة، سواء كانت متاحة أم لا.", verbose_name="حالة الخدمة")

    # التاريخ الذي تم فيه إضافة الخدمة
    created_at = models.DateTimeField(auto_now_add=True, help_text="التاريخ والوقت الذي تمت فيه إضافة الخدمة.")

    # التاريخ الذي تم فيه تعديل الخدمة آخر مرة
    updated_at = models.DateTimeField(auto_now=True, help_text="التاريخ والوقت الذي تم فيه آخر تعديل للخدمة.")

    # مرجع لصاحب المهنة الذي يقدم الخدمة
    provider = models.ForeignKey('auth.User', on_delete=models.CASCADE, help_text="صاحب المهنة الذي يقدم الخدمة.")


    geo_lat = models.CharField(max_length=254, blank=True, null=True)
    geo_lng = models.CharField(max_length=254 , blank=True, null=True)

    # المدينة أو المنطقة التي تتوفر بها الخدمة
    location = models.CharField(max_length=100, help_text="الموقع الجغرافي الذي تُقدم فيه الخدمة.", verbose_name="الموقع", null=True)
    def __str__(self):
        return self.name

    @property
    def get_rating_range(self):
        review = Review.objects.filter(service_request__service__id=self.id)
        full_comlpete_rate = 5 * review.count()
        full_rate = 0
        for r in review:
            full_rate += r.rating
        if full_comlpete_rate:
            rate = (full_rate / full_comlpete_rate * 10) / 2
        else: rate = 0

        l =  [i for i in range(1, (int(rate)+1))]
        out = []
        for i in range(1, 6):
            out.append(1) if i in l else out.append(0)
        return str(rate)
    
    @property
    def get_requests(self):
        r = ServiceRequest.objects.filter(service__id=self.id)
        return r
    
    def get_user_services(self):
        r = ServiceModel.objects.filter(provider=self.provider)
        return r
    
    @property
    def when_updated(self):
        return when_published(self.updated_at)
    

class ServiceRequest(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='service_requests')
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=10, choices=service_request_status_choices, default='pending')
    accepted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Request by {self.customer.get_full_name} for {self.service.name}"

    @property
    def when_updated(self):
        return when_published(self.created_at)
    
    class Meta:
        ordering = ['-created_at']
    
class Complaint(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    related_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint by {self.user.username}"
    

class Review(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def create_rating_range(self):
        l =  [i for i in range(1, (self.rating+1))]
        out = []
        for i in range(1, 6):
            out.append(1) if i in l else out.append(0)
        return out
    
    def __str__(self):
        return f"Review by {self.reviewer}"