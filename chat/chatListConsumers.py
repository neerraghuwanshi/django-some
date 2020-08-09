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

    @receiver(post_save, sender=Chat)
    def update_chats(sender, instance, **kwargs):
        global room_group_name
        chat = Chat.objects.get(id=instance.id)
        content = {
            'command': 'update_chats',
            'chat': ChatListConsumer.chat_to_json(chat, {'username':instance})
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(room_group_name, {
                'type': 'chat',
                'chat': content
            })


    def fetch_chats(self, data):
        chats = get_chats(data['username'], data['chatIndex'])
        content = {
            'command': 'chats',
            'chats': ChatListConsumer.chats_to_json(chats, data)
            }
        self.send_chats(content)

    def fetch_more_chats(self, data):
        chats = get_chats(data['username'],data['chatIndex'])

        content = {
            'command': 'more_chats',
            'chats': ChatListConsumer.chats_to_json(chats,data)
        }
        self.send_chats(content)

    @staticmethod
    def chats_to_json(chats, data):
        result = []
        for chat in chats:
            result.append(ChatListConsumer.chat_to_json(chat, data))
        return result

    @staticmethod
    def chat_to_json(chat, data):

        participants = chat.participants.all()
        participants_list = []
        user = ''
        for participant in participants:
            if participant != data['username']:
                user = participant
            participants_list.append(participant.username)
        contact = get_user_contact(user)
        image = UserProfile.objects.get(user=contact)
        user_image = None
        if image.image:
            user_image = image.image.url

        last_message = chat.messages.last().content

        return {
            'id': chat.id,
            'username': participants_list,
            'last_message': last_message,
            'user_image': user_image,
            'updated_at': str(chat.updated_at),
        }

    commands = {
        'fetch_chats': fetch_chats,
        'fetch_more_chats':fetch_more_chats,
    }

    def connect(self):
        global room_group_name, channel_layer
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        channel_layer = self.channel_layer
        room_group_name = 'chatList_%s' % self.room_name
        async_to_sync(channel_layer.group_add)(
            room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        global room_group_name
        async_to_sync(self.channel_layer.group_discard)(
            room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat(self, chat):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat',
                'chat': chat
            }
        )

    def send_chats(self, chats):
        self.send(text_data=json.dumps(chats))

    def chat(self, event):
        chat = event['chat']
        self.send(text_data=json.dumps(chat))