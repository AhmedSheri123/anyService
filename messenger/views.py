from django.shortcuts import render, redirect
from .models import MessagesModel, MessengerModel, FavoriteUserModel, BlockUserModel
from accounts.models import UserProfile, ServiceRequest
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages as dj_messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
# Create your views here.


def messageRoom(request, room_id):
    user = request.user

    messenger = MessengerModel.objects.get(room_id=room_id)
    receiver = messenger.messenger_users.exclude(id=user.id).first()

    if receiver.userprofile.dont_receive_msg_from_companys and user.userprofile.is_company:
        dj_messages.error(request, 'لقد الغى المستلم امكانية استقبال الرسائل')
    elif receiver.userprofile.dont_receive_msg_from_employees and user.userprofile.is_employee:
        dj_messages.error(request, 'لقد الغى المستلم امكانية استقبال الرسائل')

    is_blocked = BlockUserModel.objects.filter(creator=user, user=receiver).exists()
    receiver_block_sender = BlockUserModel.objects.filter(creator=receiver, user=user).exists()
    is_favorite = FavoriteUserModel.objects.filter(creator=user, user=receiver).exists()
    messages_list = []
    last_date = None
    msg_date = []
    messages = MessagesModel.objects.filter(messenger__room_id=room_id)
    for msg in messages:
        if last_date == None:
            last_date=msg.creation_date.date()
        elif msg.creation_date.date() != last_date:
            
            messages_list.append([last_date, msg_date])
            last_date=msg.creation_date.date()
            msg_date = []
            
        msg_date.append(msg)
    messages_list.append([last_date, msg_date])

    profile_image = receiver.userprofile.profile_img_base64
    return render(request, 'messenger/viewMessage.html', {'receiver_block_sender':receiver_block_sender, 'is_blocked':is_blocked, 'is_favorite':is_favorite, 'messages_list':messages_list, 'room_id':room_id, 'receiver':receiver, 'profile_image':profile_image})


def get_messenger_model(sender, receiver, ser_req):
    messengers = MessengerModel.objects.filter(messenger_users=sender, service_request=ser_req).filter(messenger_users=receiver)
    return messengers

def createMessager(request, receiver_id, ser_req_id):
    ser_req = ServiceRequest.objects.get(id=ser_req_id)
    sender = request.user
    receiver = User.objects.get(id=receiver_id)
    
    messengers = get_messenger_model(sender, receiver, ser_req)

    if sender != receiver:
        if not messengers.exists():    
            messenger = MessengerModel.objects.create(service_request=ser_req)
            messenger.messenger_users.set([sender, receiver])
            messenger.save()
            room_id = messenger.room_id
        else:
            room_id = messengers.first().room_id
        return redirect('messageRoom', room_id)
    else:
        return redirect('redirect_index')


def AddFavorite(request, receiver_id):
    creator = request.user
    receiver = User.objects.get(id=receiver_id)

    if not FavoriteUserModel.objects.filter(creator=creator, user=receiver).exists():
        fav = FavoriteUserModel.objects.create(creator=creator, user=receiver)
        fav.save()

    room = get_messenger_model(sender=creator, receiver=receiver).first()

    return redirect('messageRoom', room.room_id)



def AddDeleteFavorite(request, receiver_id):
    creator = request.user
    receiver = User.objects.get(id=receiver_id)

    if FavoriteUserModel.objects.filter(creator=creator, user=receiver).exists():
        fav = FavoriteUserModel.objects.filter(creator=creator, user=receiver)
        for f in fav:
            f.delete()
            return JsonResponse({'status':False})
    else:
        fav = FavoriteUserModel.objects.create(creator=creator, user=receiver)
        fav.save()
        return JsonResponse({'status':True})


def DeleteFavorite(request, fav_id):
    sender = request.user
    if request.GET.get('redir'):
        receiver = User.objects.get(id=fav_id)
        room = get_messenger_model(sender=sender, receiver=receiver).first()
        favs = FavoriteUserModel.objects.filter(creator=sender, user=receiver)
        if favs.exists():
            favs.first().delete()
        return redirect('messageRoom', room.room_id)
    else:
        if FavoriteUserModel.objects.filter(id=fav_id).exists():
            fav = FavoriteUserModel.objects.get(id=fav_id)
            receiver = fav.user

            return JsonResponse({'status':True})
        return JsonResponse({'status':False})


def BlockUserMessenger(request, receiver_id):
    creator = request.user
    receiver = User.objects.get(id=receiver_id)
    if not BlockUserModel.objects.filter(creator=creator, user=receiver).exists():
        fav = BlockUserModel.objects.create(creator=creator, user=receiver)
        fav.save()

    room = get_messenger_model(sender=creator, receiver=receiver).first()

    return redirect('messageRoom', room.room_id)

def DeleteBlockUser(request, block_id):
    sender = request.user
    if request.GET.get('redir'):
        receiver = User.objects.get(id=block_id)
        room = get_messenger_model(sender=sender, receiver=receiver).first()
        favs = BlockUserModel.objects.filter(creator=sender, user=receiver)
        if favs.exists():
            favs.first().delete()
        return redirect('messageRoom', room.room_id)
    else:
        if BlockUserModel.objects.filter(id=block_id).exists():
            fav = BlockUserModel.objects.get(id=block_id)
            fav.delete()

            return JsonResponse({'status':True})
        return JsonResponse({'status':False})

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
@csrf_exempt
def SendFiles(request, room_id):
    sender = request.user
    messenger = MessengerModel.objects.get(room_id=room_id)
    receiver = messenger.messenger_users.exclude(id=sender.id).first()
    files = request.FILES.getlist('file', '')

    for file in files:
        if file:
            message = MessagesModel.objects.create(sender=sender, msg_type='2', messenger=messenger)
            message.file = file
            message.save()
            file_name = os.path.basename(message.file.name) if message.file.name else None
            channel_layer = get_channel_layer()
            receiver_room_id = f'chat_{room_id}'

            async_to_sync(channel_layer.group_send)(
                receiver_room_id,
                        {
                            'type': 'chat_message',
                            'msg_type':'file',
                            'method':'send_msg',
                            'user_id': sender.id,
                            'receiver_id': receiver.id,
                            'msg_id': message.id,
                            'file_url': message.file.url,
                            'file_name': file_name,
                            'send_toast':False,
                            'is_active':receiver.userprofile.is_active,
                            'sender_subscription_passed':True,
                            'receiver_subscription_passed':True,
                            'receiver_subscription_end_msg':  '',
                            'creation_date': message.creation_date.strftime('%H:%M'),
                        }
            )
    return JsonResponse({'succses':True})



def DirectionMap(request):
    return render(request, 'messenger/DirectionMap.html')