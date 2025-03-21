from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PasswordResetCode, CustomUser

class PasswordResetView(APIView):
    permission_classes = []

    def post(self, request):
        phone = request.data.get('phone')

        try:
            user = CustomUser.objects.get(phone=phone)
            code = PasswordResetCode.generate_code()

            # Сохраняем код в БД
            PasswordResetCode.objects.create(user=user, code=code)

            # Заглушка для отправки SMS (реализуйте интеграцию с SMS-сервисом)
            print(f"SMS отправлен на {phone}: Ваш код подтверждения - {code}")

            return Response({"status": "Код отправлен"})

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
def check_phone_availability(request):
    phone = request.query_params.get('phone', '')

    if not phone:
        return Response(
            {"error": "Параметр 'phone' обязателен"},
            status=400
        )

    exists = CustomUser.objects.filter(phone=phone).exists()
    return Response({
        "phone": phone,
        "available": not exists
    })


class PasswordResetConfirmView(APIView):
    permission_classes = []

    def post(self, request):
        phone = request.data.get('phone')
        code = request.data.get('code')
        new_password = request.data.get('new_password')

        try:
            # Находим код подтверждения
            reset_code = PasswordResetCode.objects.get(
                user__phone=phone,
                code=code
            )

            if reset_code.is_expired():
                reset_code.delete()
                return Response(
                    {"error": "Код просрочен"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Обновляем пароль
            user = reset_code.user
            user.set_password(new_password)
            user.save()

            # Удаляем использованный код
            reset_code.delete()

            return Response(
                {"status": "Пароль успешно изменён"},
                status=status.HTTP_200_OK
            )

        except PasswordResetCode.DoesNotExist:
            return Response(
                {"error": "Неверный код или номер телефона"},
                status=status.HTTP_400_BAD_REQUEST
            )

