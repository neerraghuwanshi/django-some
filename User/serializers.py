from rest_framework import serializers
from django.contrib.auth.models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.core.validators import EmailValidator

class UserRegisterSerializer(RegisterSerializer):

    def validate_email(self, value):
        ModelClass = User
        if ModelClass.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    
    def validate_username(self, value):
        ModelClass = User
        if ModelClass.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def get_cleaned_data(self):
        super(UserRegisterSerializer, self).get_cleaned_data()
        return {
            'email': self.validated_data.get(
                'email', ''
            ),
            'username': self.validated_data.get(
                'username', ''
            ),
            'password1': self.validated_data.get(
                'password1', ''
            ),
            'first_name': self.validated_data.get(
                'first_name', ''
            ),
            'last_name': self.validated_data.get(
                'last_name', ''
            ),
        }


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 
            'email', 
            'first_name',
            'last_name',
        )
        read_only_fields = (
            'username',
            'email', 
        )

    