import re

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from registration.utils import send_verification_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']
        read_only_fields = ['id', 'email', 'is_active']
        extra_kwargs = {
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate_username(self, value):
        if self.instance and self.instance.username == value:
            return value

        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]{2,29}$', value):
            raise serializers.ValidationError("Username must be 3–30 characters, start with a letter or underscore, "
                                              "and use only letters, numbers, or underscores.")

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")

        return value

    def _validate_alpha_field(self, field_name, value):
        if not value.isalpha():
            raise serializers.ValidationError(
                f"{field_name} must contain alphabetic characters only. No digits or symbols allowed."
            )
        return value

    def validate(self, attrs):
        if 'first_name' in attrs:
            self._validate_alpha_field("First name", attrs['first_name'])
        if 'last_name' in attrs:
            self._validate_alpha_field("Last name", attrs['last_name'])

        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=8, max_length=128, write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(min_length=8, max_length=128, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        extra_kwargs = {
            'email': {
                'required': True,
                'allow_null': False,
                'allow_blank': False
            }
        }

    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]{2,29}$', value):
            raise serializers.ValidationError("Username must be 3–30 characters, start with a letter or underscore, "
                                              "and use only letters, numbers, or underscores.")

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")

        return value

    def validate_email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("Invalid email entered.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")

        return value

    def _validate_alpha_field(self, field_name, value):
        key = field_name.lower().replace(" ", "_")
        if not value.isalpha():
            raise serializers.ValidationError({
                key: f"{field_name} must contain alphabetic characters only. No digits or symbols allowed."
            })
        return value

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        self._validate_alpha_field("First name", attrs['first_name'])
        self._validate_alpha_field("Last name", attrs['last_name'])

        if password1 != password2:
            raise serializers.ValidationError({
                'password': "Passwords do not match."
            })

        try:
            validate_password(attrs['password1'], user=None)
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': e.messages})

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
            user = User.objects.get(username__iexact=username)
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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, max_length=128, write_only=True,
                                         style={'input_type': 'password'})
    new_password = serializers.CharField(min_length=8, max_length=128, write_only=True,
                                         style={'input_type': 'password'})
    confirm_new_password = serializers.CharField(min_length=8, max_length=128, write_only=True,
                                                 style={'input_type': 'password'})

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({
                'password': "New password fields didn't match."
            })
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({
                'password': "New password must be different from the old one."
            })

        try:
            validate_password(attrs['new_password'], user=self.context['request'].user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': e.messages})

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    # TODO: Implement token blacklisting logic in the view (e.g., add refresh to blacklist)


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
