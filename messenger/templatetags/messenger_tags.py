from django import template
from django.template.defaultfilters import stringfilter
from messenger.models import MessagesModel, MessengerModel, BlockUserModel, FavoriteUserModel
from django.contrib.auth.models import User
from accounts.models import UserProfile
import os

register = template.Library()

@register.simple_tag
@stringfilter
def get_messengers(user_id):
    messengers = MessengerModel.objects.filter(messenger_users__id__in=[user_id])
    for messenger in messengers:
        msgs = MessagesModel.objects.filter(messenger=messenger)
        if not msgs.exists():
            messengers = messengers.exclude(id=messenger.id)
    return messengers

@register.simple_tag
@stringfilter
def get_last_msg(messenger_id, receiver):
    messenger = MessengerModel.objects.get(id = messenger_id)
    messages = MessagesModel.objects.filter(messenger=messenger)
    messages = messages.exclude(sender=receiver)
    if messages.exists():
        msg = messages.order_by('-id').first()
        if not msg.is_receiver_subscription_passed:
            msg.msg = 'نفذ عدد استقبال الرسائل يرجى ترقية او تجديد العضوية لاظهار الرسالة'

        return msg
    return ''

@register.simple_tag
@stringfilter
def get_user_profile_img(user_id):
    if user_id:
        user = User.objects.get(id=user_id)
        img = user.userprofile.profile_img_base64

        return img

@register.simple_tag
@stringfilter
def get_receiver_user(sender_id, room_id):
    messenger = MessengerModel.objects.get(room_id=room_id)
    receiver = messenger.messenger_users.exclude(id=sender_id).first()

    return receiver

@register.simple_tag
@stringfilter
def get_favorite_users(user):
    fav = FavoriteUserModel.objects.filter(creator=user)
    return fav

@register.simple_tag
@stringfilter
def get_blocked_users(user):
    blockers = BlockUserModel.objects.filter(creator=user)
    return blockers

@register.simple_tag
@stringfilter
def get_count_of_not_readed_msg(user_id):
    count = 0
    messengers = MessengerModel.objects.filter(messenger_users__id__in=[user_id])
    for messenger in messengers:
        messages = MessagesModel.objects.filter(messenger=messenger, is_readed=False).exclude(sender__id=user_id)
        count += messages.count()
    if count >= 99:
        count  = str(count)+'+'
    if count <= 0:
        count = ''
    return count

@register.simple_tag
@stringfilter
def get_user_full_name(user_id):
    full_name = ''
    if user_id:
        user = User.objects.get(id=user_id)
        userprofiles = UserProfile.objects.filter(user=user)
        if userprofiles.exists():
            userprofile = userprofiles.first()
            full_name = userprofile.get_full_name
    return full_name
    

@register.simple_tag
@stringfilter
def get_file_name(name):
    file_name = os.path.basename(name) if name else None
    return file_name