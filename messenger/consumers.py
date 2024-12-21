import json, datetime
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import MessagesModel, MessengerModel, BlockUserModel
from accounts.models import UserProfile
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from base64 import b64decode, urlsafe_b64decode
from io import BytesIO
from django.core.files.base import ContentFile

def get_time_now_file_name():
    a = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
    return a
def DecodeAudioBase64(base64):
    # print(base64)
    decode_string = urlsafe_b64decode(base64)
    # buffer = BytesIO(decode_string)
    # buffer.seek(0)
    return decode_string

class chatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.msg_model = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        user = self.scope["user"]
        userprofile = UserProfile.objects.get(id=user.userprofile.id)
        userprofile.is_in_chat = True
        userprofile.active_messenger = MessengerModel.objects.get(room_id=self.room_name)
        userprofile.save()

        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        room = MessengerModel.objects.get(room_id=self.room_name)
        msgs_model = MessagesModel.objects.filter(messenger=room, is_readed=False)
        for i in msgs_model.exclude(sender=user):
            i.is_readed = True
            i.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'msg_read_all',
                'method':'msg_read_all',
                'user_id': user.id,
            }
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

        user = self.scope["user"]
        userprofile = UserProfile.objects.get(id=user.userprofile.id)
        userprofile.is_in_chat = False
        userprofile.save()

    def receive(self, text_data=None, bytes_data=None):


        text_data_json = json.loads(text_data)
        method = text_data_json['method']
        user = self.scope["user"]
        userprofile = UserProfile.objects.get(user=user)
        room = MessengerModel.objects.get(room_id=self.room_name)
        
        # send chat message event to the room
        print(text_data_json)
        if method == 'send_msg':
            msg_type = text_data_json['msg_type']
            receiver = room.messenger_users.exclude(id=user.id).first()
            receiver_profile = UserProfile.objects.get(user=receiver)

            is_blocked = BlockUserModel.objects.filter(creator=receiver, user=user).exists()
            his_blocked = BlockUserModel.objects.filter(creator=user, user=receiver).exists()

                    


            if is_blocked or his_blocked:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'method':'Blocked',
                    }
                )

            else:

                message = text_data_json.get('message', '')
                

                msg_model = MessagesModel.objects.create(messenger=room, sender=user)
                audio_url = ''
                send_toast = False
                is_active = receiver.userprofile.is_active
                if is_active:
                    if receiver.userprofile.is_in_chat and receiver.userprofile.active_messenger!=room:
                        send_toast = True
                    elif not receiver.userprofile.is_in_chat:
                        send_toast = True
                if msg_type == 'audio':
                    time_now = get_time_now_file_name()
                    file_name = f'audio_{time_now}.wav'
                    content_file = ContentFile(DecodeAudioBase64(message), name=file_name)
                    msg_model.audio = content_file
                    msg_model.msg_type = '4'
                    message = ''
                    msg_model.save()
                    audio_url = msg_model.audio.url
                elif msg_type == 'text':
                    msg_model.msg_type = '1'
                    msg_model.msg=message
                    msg_model.save()
                
                
                
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'msg_type':msg_type,
                        'method':method,
                        'user_id': user.id,
                        'receiver_id': receiver.id,
                        'msg_id': msg_model.id,
                        'message': message,
                        'audio_url': audio_url,
                        'send_toast':send_toast,
                        'is_active':is_active,
                        'sender_subscription_passed':True,
                        'receiver_subscription_passed':True,
                        'receiver_subscription_end_msg':  '',
                        'creation_date': msg_model.creation_date.strftime('%H:%M'),
                    }
                )

        elif method == 'msg_readed':
            msg_id = text_data_json['msg_id']
            msg_model = MessagesModel.objects.get(id=msg_id)
            msg_model.is_readed = True
            msg_model.save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'msg_readed',
                    'method':method,
                    'user_id': user.id,
                    'msg_id': msg_id,
                }
            )

        elif method == 'typing':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'typing',
                    'method':method,
                    'user_id': user.id,
                }
            )
    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def msg_readed(self, event):
        self.send(text_data=json.dumps(event))

    def msg_read_all(self, event):
        self.send(text_data=json.dumps(event))

    def showToast(self, event):
        self.send(text_data=json.dumps(event))

    def typing(self, event):
        self.send(text_data=json.dumps(event))
# code src = https://testdriven.io/blog/django-channels/, https://www.youtube.com/watch?v=cw8-KFVXpTE

