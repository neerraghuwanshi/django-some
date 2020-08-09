from django.urls import re_path
from chat.chatConsumers import ChatConsumer
from chat.chatListConsumers import ChatListConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
    re_path(r'^ws/chatList/(?P<room_name>[^/]+)/$', ChatListConsumer),
]
