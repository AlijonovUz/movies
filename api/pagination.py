from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):

        return Response({
            'data': {
                'total': self.page.paginator.count,
                'results': data
        },
            'error': None,
            'success': True,
        }, status=status.HTTP_200_OK)