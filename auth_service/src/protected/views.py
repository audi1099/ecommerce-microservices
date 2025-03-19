from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class TestAuthView(APIView):
    """
    Пример защищённого API-эндпоинта.
    Доступ только для аутентифицированных пользователей.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": f"Привет, {request.user.username}!",
            "email": request.user.email,
            "phone": request.user.phone
        })
