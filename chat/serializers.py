from rest_framework import serializers
from django.shortcuts import  get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from UserProfile.models import UserProfile
from chat.models import Chat, Message

User = get_user_model()

def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return user

class ContactSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class ChatSerializer(serializers.ModelSerializer):
    participants = ContactSerializer(many=True)
    user_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Chat
        fields = ('id', 'messages', 'participants','user_image')
        read_only = ('id')

    def get_user_image(self, obj):
        request = self.context.get("request")
        participants = obj.participants.all()
        for participant in participants:
            if participant != request.user.username:
                contact = get_user_contact(participant)
        image = UserProfile.objects.get(user=contact)
        if image.image:
            return request.build_absolute_uri(image.image.url)

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        current_chat = Chat.objects.filter(participants__username=participants[0]).filter(participants__username=participants[1])
        if current_chat.exists():
            return current_chat[0]
        new_chat = Chat()
        new_chat.save()
        for username in participants:
            contact = get_user_contact(username)
            new_chat.add(contact)
        new_chat.save()
        return chat