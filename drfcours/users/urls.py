from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .apps import UsersConfig
from .views import (
    UsersCreateAPIView,
    UsersDestroyAPIView,
    UsersListAPIView,
    UsersUpdateAPIView,
)


app_name = UsersConfig.name


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("list/", UsersListAPIView.as_view(), name="user_list"),
    path("register/", UsersCreateAPIView.as_view(), name="register"),
    path("update/", UsersUpdateAPIView.as_view(), name="user_update"),
    path("delete/", UsersDestroyAPIView.as_view(), name="user_delete"),
]
