from django.urls import path
from .views import (
    BlogListView, 
    BlogCreateView,
    BlogRetrieveDestroyView,
    BlogListUserView
)

urlpatterns = [
    path('', 
    BlogListView.as_view(), name='blog_list'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('username/<username>/', BlogListUserView.as_view(), name='blog_list_user'),
    path('detail/<int:pk>/', BlogRetrieveDestroyView.as_view(), name='blog_retrieve'),
]