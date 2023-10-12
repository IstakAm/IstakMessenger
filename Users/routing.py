from django.urls import re_path

from . import consumers

ws_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/(?P<token>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
    re_path(r'ws/message_update/(?P<key>\w+)/$', consumers.MessageUpdaterConsumer.as_asgi()),
]