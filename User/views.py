from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from dj_rest_auth.serializers import SetPasswordForm 
from rest_auth.registration.views import RegisterView
from .serializers import UserDetailsSerializer

# Create your views here.

class UserRegisterView(RegisterView):
    queryset = User.objects.all()

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer






