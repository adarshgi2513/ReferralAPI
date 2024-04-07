from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email','password', 'referral_code', 'registration_timestamp']

class LoginSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

    class Meta:
        fields = ['name', 'password']


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'referral_code', 'registration_timestamp']



class ReferralUserSerializer(serializers.ModelSerializer):
    registration_timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'registration_timestamp']