
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from users.serializers import TokenSerializer, UserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    """Кастомный view для получения JWT-токенов"""
    serializer_class = TokenSerializer


class UsersCreateAPIView(generics.CreateAPIView):
    """API-эндпоинт для регистрации нового пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Хеширует пароль перед сохранением пользователя."""
        user = serializer.save()
        user.set_password(user.password)
        user.save()


@permission_classes([IsAuthenticated])
class UsersListAPIView(generics.ListAPIView):
    """API-эндпоинт для отображения списка зарегистрированных пользователей"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


@permission_classes([IsAuthenticated])
class UsersRetrieveAPIView(generics.RetrieveAPIView):
    """API-эндпоинт для отображения информации по конкретному пользователю (detail)"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


@permission_classes([IsAuthenticated])
class UsersUpdateAPIView(generics.UpdateAPIView):
    """API-эндпоинт для изменения информации по конкретному пользователю"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


@permission_classes([IsAuthenticated])
class UsersDestroyAPIView(generics.DestroyAPIView):
    """API-эндпоинт для удаления информации по конкретному пользователю"""
    queryset = User.objects.all()
