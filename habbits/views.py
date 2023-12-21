from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from habbits.models import Habit, Prize
from habbits.paginators import HabitPrizePaginator
from habbits.permissions import IsOwner, IsPrizeOwner
from habbits.serializers import HabitSerializer, PrizeSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.habit_owner = self.request.user

        new_habit.save()


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPrizePaginator
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        queryset = Habit.objects.filter(habit_owner=self.request.user)
        return queryset


class HabitPublicListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPrizePaginator
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Habit.objects.filter(habit_is_public=True)
        return queryset


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PrizeCreateAPIView(generics.CreateAPIView):
    serializer_class = PrizeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_prize = serializer.save()
        new_prize.prize_owner = self.request.user

        new_prize.save()


class PrizeListAPIView(generics.ListAPIView):
    serializer_class = PrizeSerializer
    permission_classes = [IsAuthenticated, IsPrizeOwner]
    pagination_class = HabitPrizePaginator

    def get_queryset(self):
        queryset = Prize.objects.filter(prize_owner=self.request.user)
        return queryset


class PrizeRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()
    permission_classes = [IsAuthenticated, IsPrizeOwner]


class PrizeUpdatePIView(generics.UpdateAPIView):
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()
    permission_classes = [IsAuthenticated, IsPrizeOwner]


class PrizeDestroyPIView(generics.DestroyAPIView):
    queryset = Prize.objects.all()
    permission_classes = [IsAuthenticated, IsPrizeOwner]
