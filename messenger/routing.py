from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/messanger/(?P<room_name>\w+)/$', consumers.chatConsumer.as_asgi())
]
