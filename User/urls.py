from django.urls import path, include, re_path
from .views import UserRegisterView

urlpatterns = [
    path('',UserRegisterView.as_view(),name='user_create')
]