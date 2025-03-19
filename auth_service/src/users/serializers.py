from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import phonenumbers
from phonenumbers import NumberParseException
from .models import CustomUser
from rest_framework.validators import UniqueValidator

# Для JWT
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

# Для регистрации
class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(),
                message="Этот номер телефона уже зарегистрирован"
            )
        ]
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_phone(self, value):
        try:
            parsed = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed):
                raise serializers.ValidationError("Неверный формат номера")
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        except NumberParseException:
            raise serializers.ValidationError("Некорректный номер телефона")