from rest_framework import serializers

from habbits.models import Habit, Prize
from habbits.validators import validator_for_habit


class HabitSerializer(serializers.ModelSerializer):
    """ сериализатор для модели Habit """

    class Meta:
        model = Habit
        fields = '__all__'

        validators = [
            validator_for_habit,
        ]


class PrizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prize
        fields = '__all__'
