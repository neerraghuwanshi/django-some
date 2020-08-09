from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_profile')
    followers = models.ManyToManyField(User,related_name='following',blank=True)
    following = models.ManyToManyField(User,related_name='followers',blank=True)
    bio = models.TextField(blank=True, null=True)
    image=models.ImageField(blank=True,null=True,upload_to="profile_images/")
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None


def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=User)