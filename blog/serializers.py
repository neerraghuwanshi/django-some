from rest_framework import serializers
from .models import blog, Comment
from UserProfile.models import UserProfile


class blogSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    author_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = blog
        fields = [
            'id',
            'caption',
            'author',
            'likes',
            'is_liked',
            'media',
            'created',
            'updated_at',
            'author_image'
        ]
        extra_field_kwargs = {'url': {'lookup_field': 'username'}}

    def get_author(self, obj):
        return obj.author.username

    def get_is_liked(self, obj):
        is_liked = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            is_liked = user in obj.likes.all()
        return is_liked
    
    def get_author_image(self, obj):
        request = self.context.get("request")
        profile = UserProfile.objects.get(user__username=obj.author)
        if profile.image:
            return request.build_absolute_uri(profile.image.url)

    
class CommentSerializer(serializers.ModelSerializer):
    commentor = serializers.SerializerMethodField(read_only=True)
    commentor_image = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'comment',
            'commentor',
            'commentor_image',
        ]
        
    def get_commentor(self, obj):
        return obj.commentor.username
    
    def get_commentor_image(self, obj):
        request = self.context.get("request")
        profile = UserProfile.objects.get(user__username=obj.commentor)
        if profile.image:
            return request.build_absolute_uri(profile.image.url)