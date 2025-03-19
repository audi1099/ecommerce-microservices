from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser

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

