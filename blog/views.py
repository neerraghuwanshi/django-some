from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,RetrieveDestroyAPIView, ListAPIView
from rest_framework.permissions import BasePermission
from rest_framework import mixins
from rest_framework.pagination import CursorPagination
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from .models import blog
from .permissions import IsOwnerOrReadOnly

from .models import blog
from .serializers import blogSerializer
from django.contrib.auth.models import User


class Pagination(CursorPagination):
    page_size=10
    page_size_query_param=page_size
    ordering=['-id']

class BlogListView(ListAPIView):
    serializer_class = blogSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class=Pagination

    def get_queryset(self):
        return blog.objects.feed(self.request.user)

    def get_object(self):
        return self.get_queryset()


class BlogCreateView(CreateAPIView):
    serializer_class = blogSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (JSONParser,FormParser, MultiPartParser,)

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)


class BlogListUserView(ListAPIView):
    serializer_class = blogSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.kwargs['username'] 
        if user:
            return blog.objects.filter(author__username=user)
        return blog.objects.feed(self.request.user)

    def get_object(self):
        return self.get_queryset()
    
    
class BlogRetrieveDestroyView(RetrieveDestroyAPIView):
    queryset = blog.objects.all()
    serializer_class = blogSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        action = request.GET.get('action')
        blog = self.get_object()
        if action == 'like':
            blog.likes.add(request.user) 
            blog.is_liked = True
        if action == 'unlike':
            blog.likes.remove(request.user) 
            blog.is_liked = False
        serializer = self.get_serializer(blog)
        return Response(serializer.data)
