from django.db import models

# Create your models here.

SubscriptionsTheemChoices = (
    ('primary', 'primary'),
    ('secondary', 'secondary'),
    ('success', 'success'),
    ('danger', 'danger'),
    ('warning', 'warning'),
    ('info', 'info'),
    ('light', 'light'),
    ('dark', 'dark'),
)

plan_type_choices = [
    ('premium', 'Premium'),
    ('pro', 'PRO'),
    ('basic', 'Basic'),
]

plan_scope_choices = [
    ('1', 'شهري'),
    ('2', 'سنوي')
]

CurrencyChoices = (
    ("SAR", "ريال سعودي"),
    ("USD", "دولار"),
    ("EUR", "يورو"),
)

class SubscriptionsModel(models.Model):
    title = models.CharField(max_length=255, verbose_name='العنوان')

    Theem = models.CharField(max_length=255, choices=SubscriptionsTheemChoices, null=True, verbose_name='الثيم')
    plan_type = models.CharField(max_length=255, choices=plan_type_choices, null=True, verbose_name='نو الاشتراك')

    plan_scope = models.CharField(max_length=255, choices=plan_scope_choices, null=True, verbose_name='مدة الاشتراك')
    price = models.DecimalField(max_digits=6, null=True, decimal_places=2, verbose_name='السعر')
    discont = models.IntegerField(default=0, null=True, verbose_name='خصم')

    currency = models.CharField(max_length=250, choices=CurrencyChoices, default='USD', null=True, verbose_name='العملة')    
    is_enabled = models.BooleanField(default=True, verbose_name='هل الاشتراك مفعل ليظهر على الموقع')

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

    def __str__(self):
        return str(self.title)
