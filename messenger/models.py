from django.db import models
from django.contrib.auth.models import User
import string
import random
from accounts.libs import when_published
from accounts.models import ServiceRequest
# Create your models here.


msg_type_choices = (
    ('1', 'text'),
    ('2', 'file'),
    ('3', 'location'),
    ('4', 'audio'),
)

def RandomRoomIDGen():
    N = 25
    res = ''.join(random.choices(string.digits, k=N))
    return 'i' + str(res)


class MessengerModel(models.Model):
    messenger_users = models.ManyToManyField(User)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    room_id = models.CharField(max_length=255, default=RandomRoomIDGen)

    creation_date = models.DateTimeField(null=True, verbose_name="تاريخ الانشاء")

class MessagesModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    msg = models.TextField(blank=True)
    msg_type = models.CharField(max_length=50, choices=msg_type_choices)
    messenger = models.ForeignKey(MessengerModel, on_delete=models.CASCADE)
    audio = models.FileField(upload_to='messanger/audio/%Y/%m/%d/', null=True, blank=True)
    file = models.FileField(upload_to='messanger/file/%Y/%m/%d/', null=True, blank=True)
    is_readed = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="تاريخ الانشاء")

    def whenpublished(self):
        return when_published(self.creation_date)
    


class BlockUserModel(models.Model):
    creator = models.ForeignKey(User, related_name="block_creator", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="block_user", on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="تاريخ الانشاء")

class FavoriteUserModel(models.Model):
    creator = models.ForeignKey(User, related_name="favorite_creator", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="favorite_user", on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="تاريخ الانشاء")