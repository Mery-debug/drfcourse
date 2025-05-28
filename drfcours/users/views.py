from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import UserSerializer, TokenSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenSerializer


class UsersCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


@permission_classes([IsAuthenticated])
class UsersListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@permission_classes([IsAuthenticated])
class UsersRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@permission_classes([IsAuthenticated])
class UsersUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@permission_classes([IsAuthenticated])
class UsersDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
