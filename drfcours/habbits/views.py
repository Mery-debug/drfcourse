from .models import Habits
from .paginators import Pagination
from .permissions import OwnerOrReadOnly
from .serializers import HabitSerializer, PublicHabitSerializer
from rest_framework import generics, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """Публичный доступ к привычкам для всех пользователей"""

    queryset = Habits.objects.filter(is_public=True)
    serializer_class = PublicHabitSerializer
    permission_classes = [AllowAny]


class HabitListAPIView(generics.ListAPIView):
    """Эндпоинт закрытого доступа только к списку своих привычек пользователя"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Эндпоинт закрытого доступа к конкретной привычке"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, OwnerOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["habits_id"] = self.kwargs["pk"]
        return context


class HabitCreateAPIView(generics.CreateAPIView):
    """Эндпоинт создания привычки только для авторизованных пользователей"""

    serializer_class = HabitSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт изменения привычки только для авторизованного владельца привычки"""

    serializer_class = HabitSerializer
    authentication_classes = [SessionAuthentication, OwnerOrReadOnly]
    queryset = Habits.objects.all()


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт удаления привычки только для авторизованного владельца привычки"""

    queryset = Habits.objects.all()
    authentication_classes = [SessionAuthentication, OwnerOrReadOnly]
    serializer_class = HabitSerializer
