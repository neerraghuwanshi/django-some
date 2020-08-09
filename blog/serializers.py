from rest_framework import serializers
from .models import blog
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
            'image',
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
        image = UserProfile.objects.filter(user__username=obj.author)
        if image[0].image:
            return request.build_absolute_uri(image[0].image.url)

    
