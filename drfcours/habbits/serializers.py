from datetime import timedelta

from dateutils import minutes
from rest_framework import serializers

from .models import Habits


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = (
            "id",
            "move",
            "place",
            "good_hab",
            "time",
            "linked_hab",
            "periodicity",
            "reward",
            "execution_time",
            "is_public",
            "owner",
        )
        read_only_fields = ("user",)

    def validate(self, data):
        """Валидация привычек на уровне сериалайзера"""
        good_hab = data.get("good_hab", False)
        reward = data.get("reward")
        linked_hab = data.get("linked_hab")
        time_to_complete = data.get("time_to_complete")
        periodicity = data.get("periodicity", 1)
        is_public = data.get("is_public", False)
        if good_hab:
            if reward:
                raise serializers.ValidationError(
                    "Приятная привычка не может иметь вознаграждение!"
                )
            if linked_hab:
                raise serializers.ValidationError(
                    "Приятная привычка не может быть связанной!"
                )
            return data
        if reward and linked_hab:
            raise serializers.ValidationError(
                "Можно указать либо вознаграждение, либо связанную привычку, но не оба!"
            )
        if linked_hab and not linked_hab.good_hab:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной!"
            )
        if time_to_complete and time_to_complete > timedelta(minutes=2):
            raise serializers.ValidationError(
                "Время выполнения не может превышать 120 секунд!"
            )
        if periodicity and periodicity > 7:
            raise serializers.ValidationError(
                "Периодичность не может быть реже чем 1 раз в 7 дней!"
            )
        if is_public and not good_hab:
            if not reward and not linked_hab:
                raise serializers.ValidationError(
                    "Публичная привычка должна иметь либо вознаграждение, либо связанную привычку!"
                )

        return data

    def create(self, validated_data):
        """Проверенные данные"""
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class PublicHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = ["id", "place", "time", "move", "periodicity", "execution_time"]
