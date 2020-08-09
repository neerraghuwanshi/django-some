from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from UserProfile.models import UserProfile

# Create your models here.

class TweetQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(author__username__iexact=username)

    def feed(self, user):
        profiles_exist = user.following.exists()
        following_user_id = []
        if profiles_exist:
            following_user_id = user.following.values_list("user__id", flat=True) 
        return self.filter(
            Q(author__id__in=following_user_id) |
            Q(author=user)
        ).distinct()
    

class TweetManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TweetQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)

    def by_username(self, username):
        return self.get_queryset().by_username(username)


class blog(models.Model):
        id = models.AutoField(primary_key=True)
        caption = models.CharField(max_length=300, null=True, blank=True)
        author = models.ForeignKey(User,related_name='blog_author', on_delete=models.CASCADE,null=True)
        created = models.TimeField(auto_now_add=True)
        updated_at = models.TimeField(auto_now=True)
        image = models.ImageField(blank=True, null=True, upload_to='images/')
        likes = models.ManyToManyField(User,related_name='liking_user',blank=True)

        objects = TweetManager()

        def __str__(self):
            if self.caption:                    return self.caption
            return self.id


        
