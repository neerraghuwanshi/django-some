from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from .serializers import UserDetailsSerializer

# Create your views here.


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer