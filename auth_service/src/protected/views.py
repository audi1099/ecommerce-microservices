from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class TestAuthView(APIView):
    permission_classes = [IsAuthenticated]

    # GET-метод
    def get(self, request, *args, **kwargs):  # Добавьте аргументы
        return Response({
            "message": f"Привет, {request.user.username}!",
            "email": request.user.email,
            "phone": request.user.phone
        })

    # POST-метод
    def post(self, request, *args, **kwargs):  # Добавьте аргументы
        return Response({"message": "POST request allowed!"})