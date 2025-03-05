from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def exception(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_msg = response.data

        if isinstance(error_msg, str):
            error_msg = {'detail': error_msg}
        elif not isinstance(error_msg, dict):
            error_msg = {'detail': 'Xatolik yuz berdi.'}

        error_msg = error_msg.get('detail', error_msg)

        return Response({
            'data': None,
            'error': {
                'errorId': response.status_code,
                'isFriendly': True,
                'errorMsg': error_msg
            },
            'success': False
        }, status=response.status_code)

    return Response({
        'data': None,
        'error': {
            'errorId': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'isFriendly': False,
            'errorMsg': "Internal server error."
        },
        'success': False
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
