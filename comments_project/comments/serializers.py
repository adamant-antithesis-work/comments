from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    login = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('login', 'username', 'email', 'home_page', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()
