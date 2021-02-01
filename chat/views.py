from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from chat.models import Chat
from chat.serializers import ChatSerializer

User = get_user_model()

def get_messages(chatId, messageIndex):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[messageIndex:messageIndex+20]


def get_chats(username, chatIndex):
    chats = Chat.objects.filter(participants__username=username)
    return chats
    # return chats[chatIndex:chatIndex+20]


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return user


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)


class ChatListView(ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        contact = get_user_contact(self.request.user.username)
        queryset = contact.chats.all().order_by('-updated_at')
        return queryset


class ChatDetailView(RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.AllowAny, )


class ChatCreateView(CreateAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
        

class ChatUpdateView(UpdateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChatDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )