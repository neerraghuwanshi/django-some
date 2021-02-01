from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Message(models.Model):
    contact = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contact.username


class Chat(models.Model):
    participants = models.ManyToManyField(
        User, related_name='chats')
    messages = models.ManyToManyField(Message)
    updated_at = models.DateTimeField(auto_now=True)
    visited = models.ManyToManyField(User, related_name='visited')

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return "{}".format(self.pk)
