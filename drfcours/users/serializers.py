from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
        )


class TokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        """Сераилизатор токена для регистрации и авторизации пользователя"""
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return token
