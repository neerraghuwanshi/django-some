from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .serializers import  UserProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import UserProfile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from blog.models import blog

class UserProfileView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'username'
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = UserProfile.objects.all()
    
    def get_object(self):
        return self.queryset.get(user__username=self.kwargs.get('username'))

    def retrieve(self, request, *args, **kwargs):
        action = request.GET.get('action')
        user_profile = self.get_object()
        user = User.objects.get(username=self.kwargs['username'])
        if request.user != user:
            requested_user_profile = UserProfile.objects.get(user=request.user)
            if (action == 'follow'):
                user_profile.followers.add(request.user) 
                requested_user_profile.following.add(user) 
            if action == 'unfollow':
                user_profile.followers.remove(request.user) 
                requested_user_profile.following.remove(user) 
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        request.user.first_name = request.data.get('first_name','')
        request.user.last_name = request.data.get('last_name','')
        request.user.save()
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)