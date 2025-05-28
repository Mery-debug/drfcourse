from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from drfcours.habbits.models import Habits
from drfcours.habbits.paginators import Pagination
from drfcours.habbits.permissions import OwnerOrReadOnly
from drfcours.habbits.serializers import HabitSerializers


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializers
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination

    def get_queryset(self):
        return Habits.objects.filter(owner=self.request.user)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializers
    permission_classes = [IsAuthenticated, OwnerOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['habits_id'] = self.kwargs['pk']
        return context


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializers
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializers
    authentication_classes = [SessionAuthentication, OwnerOrReadOnly]
    queryset = Habits.objects.all()


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habits.objects.all()
    authentication_classes = [SessionAuthentication, OwnerOrReadOnly]
    serializer_class = HabitSerializers
