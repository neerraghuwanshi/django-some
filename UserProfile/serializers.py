from rest_framework import serializers
from .models import UserProfile
from blog.models import blog

class UserProfileSerializer(serializers.ModelSerializer):

    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    posts = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "id",
            "bio",
            "following",
            "followers",
            "follower_count",
            "following_count",
            "is_following",
            "username",
            "posts",
            "image"
        ]
        extra_field_kwargs = {'url': {'lookup_field': 'username'}}
    
    def get_is_following(self, obj):
        # request???
        is_following = False
        request = self.context.get("request")
        if request:
            user = request.user
            is_following = user in obj.followers.all()
        return is_following
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name
    
    def get_username(self, obj):
        return obj.user.username
    
    def get_following_count(self, obj):
        return obj.following.count()
    
    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_posts(self, obj):
        return blog.objects.filter(author=obj.user).count()



    

