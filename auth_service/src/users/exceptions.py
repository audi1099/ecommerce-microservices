from rest_framework.views import exception_handler
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Обработка ошибок уникальности
    if isinstance(exc, IntegrityError):
        if 'phone' in str(exc):
            return Response(
                {"error": "Этот номер телефона уже зарегистрирован"},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif 'username' in str(exc):
            return Response(
                {"error": "Этот логин уже занят"},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Обработка других ошибок
    return response