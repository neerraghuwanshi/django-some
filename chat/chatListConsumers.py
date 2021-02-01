from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from chat.views import get_user_contact, get_current_chat, get_chats
from django.core import serializers
from UserProfile.models import UserProfile
from chat.models import Message, Chat
from django.db.models.signals import post_save
from django.dispatch import receiver
import channels.layers
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


User = get_user_model()

class ChatListConsumer(WebsocketConsumer):

    def fetch_chats(self, data):
        chats = get_chats(data['username'], data['chatIndex'])
        content = {
            'command': 'chats',
            'chats': self.chats_to_json(chats, data),
        }
        self.send_chats(content)

    def fetch_more_chats(self, data):
        chats = get_chats(data['username'], data['chatIndex'])

        content = {
            'command': 'more_chats',
            'chats': self.chats_to_json(chats, data)
        }
        self.send_chats(content)

    def chats_to_json(self, chats, data):
        result = []
        for chat in chats:
            result.append(self.chat_to_json(chat, data))
        return result

    def chat_to_json(self, chat, data):
        participants = chat.participants.all()
        participants_list = []
        user = ''
        for participant in participants:
            if participant.username != data['username']:
                user = participant
            participants_list.append(participant.username)
        contact = get_user_contact(user)
        user_profile = UserProfile.objects.get(user=contact)
        user_image = None
        if user_profile.image:
            user_image = user_profile.image.url

        last_message = chat.messages.last().content

        current_user = get_user_contact(data['username'])
        visited = current_user in chat.visited.all()

        return {
            'id': chat.id,
            'username': participants_list,
            'last_message': last_message,
            'visited': visited,
            'user_image': user_image,
            'updated_at': str(chat.updated_at),
        }

    commands = {
        'fetch_chats': fetch_chats,
        'fetch_more_chats': fetch_more_chats,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chatList_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    # def send_chat(self, chat):
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'chat',
    #             'chat': chat
    #         }
    #     )

    def send_chats(self, chats):
        self.send(text_data=json.dumps(chats))

    # def chat(self, event):
    #     chat = event['chat']
    #     self.send(text_data=json.dumps(chat))