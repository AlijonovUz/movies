from django.utils.deprecation import MiddlewareMixin
from rest_framework.permissions import SAFE_METHODS
from django.http import JsonResponse
from rest_framework import status

from .models import BlacklistedAccessToken


class BlackListAccessTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method not in SAFE_METHODS:
            headers = request.headers.get('Authorization', '')
            if headers.startswith('Bearer '):
                token = headers.split(' ')[1]
                if BlacklistedAccessToken.objects.filter(token=token).exists():
                    return JsonResponse({
                        'data': None,
                        'error': {
                            'errorId': status.HTTP_403_FORBIDDEN,
                            'isFriendly': True,
                            'errorMsg': "This token has been revoked. Please log in again."
                        },
                        'success': False
                    }, status=status.HTTP_403_FORBIDDEN)
