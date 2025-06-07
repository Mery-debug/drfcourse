from django.urls import path
from habbits.apps import HabbitsConfig
from habbits.views import (
    HabitCreateAPIView,
    HabitDestroyAPIView,
    HabitListAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
    PublicHabitViewSet
)
from rest_framework.routers import DefaultRouter

app_name = HabbitsConfig.name

router = DefaultRouter()
router.register(r"public-habits", PublicHabitViewSet, basename="public-habits")

urlpatterns = [
    path("create/", HabitCreateAPIView.as_view(), name="habits_create"),
    path("list/", HabitListAPIView.as_view(), name="habits_list"),
    path("retrieve/<int:pk>/", HabitRetrieveAPIView.as_view(), name="habits_retrieve"),
    path("delete/<int:pk>/", HabitDestroyAPIView.as_view(), name="habits_delete"),
    path("update/<int:pk>/", HabitUpdateAPIView.as_view(), name="habits_update"),
]+ router.urls
