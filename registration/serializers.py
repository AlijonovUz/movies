import re

from django.contrib.auth.models import User
from rest_framework import serializers


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=8, max_length=128, write_only=True)
    password2 = serializers.CharField(min_length=8, max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        extra_kwargs = {
            'email': {
                'required': True,
                'allow_null': False,
                'allow_blank': False
            }
        }

    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError('Username can only contain letters, numbers, and underscores.')

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username is already taken.')

        return value

    def validate_email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError('Invalid email entered.')
        return value

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError('Passwords do not match.')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password1')
        )

        return user
