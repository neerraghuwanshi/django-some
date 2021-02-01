from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.generics import CreateAPIView,RetrieveDestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from .models import blog, Comment
from UserProfile.models import UserProfile
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .serializers import blogSerializer, CommentSerializer
from django.contrib.auth.models import User


class Pagination(PageNumberPagination):
    page_size=10
    
class CommentPagination(PageNumberPagination):
    page_size=20
    

class BlogListView(ListAPIView):
    serializer_class = blogSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = Pagination

    def get_queryset(self):
        return blog.objects.feed(self.request.user)

    def get_object(self):
        return self.get_queryset()


class BlogCreateView(CreateAPIView):
    serializer_class = blogSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (JSONParser, FormParser, MultiPartParser,)

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)


class BlogListUserView(ListAPIView):
    serializer_class = blogSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = Pagination

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
    
       
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CommentCreateView(request):
    comment = request.data.get('comment')
    id = request.data.get('id')
    print(1)
    C = Comment.objects.create(comment=comment, commentor=request.user)
    blog.objects.get(id=id).comments.add(C)
    image = UserProfile.objects.get(user=request.user).image
    if image:
        image = image.url
    data = {
        'id': C.id,
        'comment': C.comment,
        'commentor': C.commentor.username,
        'commentor_image': request.build_absolute_uri(image),
    }
    return Response(data, status=HTTP_201_CREATED)
        
        
class CommentListView(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CommentPagination

    def get_queryset(self):
        id = self.kwargs['id']
        return blog.objects.get(id=id).comments.all()

    def get_object(self):
        return self.get_queryset()