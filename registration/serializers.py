import re

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from registration.utils import send_verification_email


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=8, max_length=128, write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(min_length=8, max_length=128, write_only=True, style={'input_type': 'password'})

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
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]{2,29}$', value):
            raise serializers.ValidationError(
                "Username must start with a letter or underscore, "
                "and be 3–30 characters long, using only letters, numbers, or underscores."
            )

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already in use.")

        return value

    def validate_email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("Invalid email entered.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")

        return value

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        if password1 != password2:
            raise serializers.ValidationError({
                'password': "Passwords do not match."
            })

        if not re.search(r'[A-Z]', password1):
            raise serializers.ValidationError({
                'password': "Password must contain at least one uppercase letter."
            })

        if not re.search(r'[a-z]', password1):
            raise serializers.ValidationError({
                'password': "Password must contain at least one lowercase letter."
            })

        if not re.search(r'\d', password1):
            raise serializers.ValidationError({
                'password': "Password must contain at least one digit."
            })

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')

        user = User.objects.create_user(
            password=password,
            is_active=False,
            **validated_data
        )

        request = self.context.get('request')
        if request:
            send_verification_email(user, request)

        return user


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]{2,29}$', username):
            raise serializers.ValidationError({
                'username': "Username must start with a letter or underscore, "
                            "and be 3–30 characters long, using only letters, numbers, or underscores."
            })

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'username': "This username is not registered."
            })

        if not user.check_password(password):
            raise serializers.ValidationError({
                'password': "Password is incorrect."
            })

        if not user.is_active:
            raise serializers.ValidationError({
                'username': "This user is not verified yet."
            })

        data = super().validate({
            'username': user.username,
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


class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=128, write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': "No user with this email address."})

        if not user.check_password(password):
            raise serializers.ValidationError({'password': "Password is incorrect."})

        if user.is_active:
            raise serializers.ValidationError({'email': "This user is already verified."})

        self.context['user'] = user
        return attrs
