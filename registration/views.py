from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer
from .permissions import IsNotAuthenticated
from .models import BlacklistedAccessToken, MyUser


class RegisterView(generics.CreateAPIView):
    queryset = MyUser
    serializer_class = RegisterSerializer
    permission_classes = [IsNotAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'data': serializer.data,
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
