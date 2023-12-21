from datetime import timedelta

from django.conf import settings
from django.db import models


class Prize(models.Model):
    prize_name = models.CharField(max_length=150, verbose_name='название награды')
    prize_description = models.TextField(blank=True, null=True, verbose_name='описание награды')
    prize_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец',
                                    blank=True, null=True)

    def __str__(self):
        return f'{self.prize_name}'

    class Meta:
        verbose_name = 'награда'
        verbose_name_plural = 'награды'
        ordering = ('prize_name',)


class Habit(models.Model):
    PERIOD_DAILY = 'ежедневно'
    PERIOD_WEEKLY = 'еженедельно'

    PERIOD_CHOICES = (
        (PERIOD_DAILY, 'ежедневно'),
        (PERIOD_WEEKLY, 'еженедельно'),
    )

    habit_user = models.CharField(max_length=100, verbose_name='пользователь')
    habit_name = models.CharField(max_length=150, verbose_name='название привычки')
    habit_place = models.CharField(max_length=200, blank=True, null=True, verbose_name='место выполнения привычки')
    habit_time = models.TimeField(blank=True, null=True, verbose_name='время выполнения привычки')
    habit_action = models.CharField(max_length=200, verbose_name='действие привычки')
    habit_is_nice = models.BooleanField(default=True, verbose_name='признак приятной привычки')
    connected_habit = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='связанная привычка')
    habit_period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default=PERIOD_DAILY,
                                    verbose_name='периодичность привычки')
    habit_prize = models.ForeignKey(Prize, on_delete=models.CASCADE, blank=True, null=True, verbose_name='приз')
    habit_duration = models.DurationField(default=timedelta(minutes=2),
                                          verbose_name='продолжительность выполнения привычки')
    habit_is_public = models.BooleanField(default=True, verbose_name='признак публичной привычки')

    habit_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец',
                                    blank=True, null=True)

    def __str__(self):
        return f'{self.habit_user} - {self.habit_name}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        ordering = ('habit_name',)
