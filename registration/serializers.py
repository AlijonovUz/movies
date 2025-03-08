import re

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import MyUser


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=8, max_length=128, write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(min_length=8, max_length=128, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = MyUser
        fields = ['phone', 'email', 'password1', 'password2']
        extra_kwargs = {
            'email': {
                'required': True,
                'allow_null': False,
                'allow_blank': False
            }
        }

    def validate_phone(self, value):
        if not re.match(r'^\+998\d{9}$', value):
            raise serializers.ValidationError({'phone': "The entered phone number is invalid."})

        if MyUser.objects.filter(phone=value).exists():
            raise serializers.ValidationError({'phone': "This phone number is already in use."})

        return value

    def validate_email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError({'email': "Invalid email entered."})

        if not MyUser.objects.filter(email=value).exists():
            raise serializers.ValidationError({'email': "This email is already in use."})

        return value

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        if password1 != password2:
            raise serializers.ValidationError({
                'password1': "Passwords do not match.",
                'password2': "Passwords do not match."
            })

        if not re.search(r'[A-Z]', password1):
            raise serializers.ValidationError({
                'password1': "Password must contain at least one uppercase letter.",
                'password2': "Password must contain at least one uppercase letter."
            })

        if not re.search(r'[a-z]', password1):
            raise serializers.ValidationError({
                'password1': "Password must contain at least one lowercase letter.",
                'password2': "Password must contain at least one lowercase letter."
            })

        if not re.search(r'\d', password1):
            raise serializers.ValidationError({
                'password1': "Password must contain at least one digit.",
                'password2': "Password must contain at least one digit."
            })

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        user = MyUser.objects.create_user(
            phone=validated_data.get('phone'),
            email=validated_data.get('email'),
            password=validated_data.get('password1')
        )

        return user


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if not re.match(r'^\+998\d{9}$', phone):
            raise serializers.ValidationError({
                'phone': "The entered phone number is invalid."
            })

        try:
            user = MyUser.objects.get(phone=phone)
        except MyUser.DoesNotExist:
            raise serializers.ValidationError({
                'phone': "This phone number is not registered."
            })

        if not user.check_password(password):
            raise serializers.ValidationError({
                'password': "Password is incorrect."
            })

        if not user.is_active:
            raise serializers.ValidationError({
                'phone': "This account has been blocked."
            })

        data = super().validate({
            'phone': user.phone,
            'password': password
        })

        return {
            'data': {
                'access': data.get('access'),
                'refresh': data.get('refresh'),
                'user': {
                    'userId': user.id,
                    'first_name': user.first_name or None,
                    'last_name': user.last_name or None,
                    'is_active': user.is_active
                }
            },
            'error': None,
            'success': True
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
