from rest_framework import serializers

from cucks.models import Cuck
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class CuckSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user = UserSerializer()

    class Meta:
        model = Cuck
        fields = ['id', 'nick', 'user', 'password']

    def create(self, validated_data):
        user = validated_data.pop('user')
        password = validated_data.pop('password')

        user = User.objects.create(username=user['username'], email=user['email'], password=password)
        cuck = Cuck.objects.create(nick=validated_data['nick'], user=user)

        return cuck


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)

