from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *
from .permissions import IsNotAuthenticated
from .models import BlacklistedAccessToken


class UserView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'data': serializer.data,
            'error': None,
            'success': True
        })

    def _save_and_respond(self, request, partial):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {
            'data': serializer.data,
            'error': None,
            'success': True
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        return self._save_and_respond(request, partial=False)

    def partial_update(self, request, *args, **kwargs):
        return self._save_and_respond(request, partial=True)


class RegisterView(generics.CreateAPIView):
    queryset = User
    serializer_class = RegisterSerializer
    permission_classes = [IsNotAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'data': {
                'user': serializer.data,
                'message': (
                    "Ro‘yxatdan o‘tish muvaffaqiyatli yakunlandi. "
                    "Email manzilingizga tasdiqlash havolasi yuborildi. "
                    "Iltimos, pochtangizni tekshiring va akkauntingizni 5 daqiqa ichida tasdiqlang. "
                    "Aks holda tasdiqlash havolasi eskiradi va qayta yuborishingiz kerak bo‘ladi."
                )
            },
            'error': None,
            'success': True
        }, status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data.get('refresh')
        token = RefreshToken(refresh)
        token.blacklist()

        headers = request.headers.get('Authorization', '')
        if headers.startswith('Bearer '):
            access = headers.split(' ')[1]
            BlacklistedAccessToken.objects.create(token=access)

        return Response({
            'error': None,
            'success': True
        }, status=status.HTTP_200_OK)


class VerifyEmailView(APIView):
    permission_classes = [IsNotAuthenticated]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user.is_active:
            return Response({
                'data': None,
                'error': {
                    'errorId': status.HTTP_400_BAD_REQUEST,
                    'isFriendly': True,
                    'errorMsg': "User is already verified."
                },
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({
                'data': {
                    'message': "Email verified successfully."
                },
                'error': None,
                'success': True
            }, status=status.HTTP_200_OK)

        return Response({
            'data': None,
            'error': {
                'errorId': status.HTTP_400_BAD_REQUEST,
                'isFriendly': True,
                'errorMsg': "Invalid or expired verification link."
            },
            'success': False
        }, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationEmailView(generics.CreateAPIView):
    serializer_class = ResendVerificationEmailSerializer
    permission_classes = [IsNotAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'data': {
                'message': "The confirmation email has been resent."
            },
            'error': None,
            'success': True
        }, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        user = serializer.context['user']
        request = self.request

        send_verification_email(user, request)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'data': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'message': "Password successfully changed."
            },
            'error': None,
            'success': True
        }, status=status.HTTP_200_OK)
