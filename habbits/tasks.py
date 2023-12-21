from datetime import datetime

import pytz
from celery import shared_task

from habbits.models import Habit
from habbits.services import create_massage


@shared_task
def check_habits_daily():

    date_time_now = datetime.now()
    moscow_timezone = pytz.timezone('Europe/Moscow')
    date_now = date_time_now.astimezone(moscow_timezone)
    time_now = date_now.time()

    habits = Habit.objects.filter(habit_time__hour=time_now.hour, habit_time__minute=time_now.minute,
                                  habit_period='ежедневно', habit_is_nice=False)

    for habit in habits:
        create_massage(habit.id)


@shared_task
def check_habits_weekly():

    date_time_now = datetime.now()
    moscow_timezone = pytz.timezone('Europe/Moscow')
    date_now = date_time_now.astimezone(moscow_timezone)
    time_now = date_now.time()

    habits = Habit.objects.filter(habit_time__hour=time_now.hour, habit_time__minute=time_now.minute,
                                  habit_period='еженедельно', habit_is_nice=False)

    for habit in habits:
        create_massage(habit.id)
