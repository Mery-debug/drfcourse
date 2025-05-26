from rest_framework import serializers

from drfcours.habbits.models import Habits


class HabitSerializers(serializers.ModelSerializer):

    class Meta:
        model = Habits
        fields = ("id", "move", "place","good_hab", "linked_hab", "periodicity", "reward", "execution_time", "is_public", "owner")

