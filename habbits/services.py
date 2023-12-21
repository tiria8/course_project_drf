import requests
from django.http import HttpResponse
import time

from config.settings import TELEGRAM_ACCESS_TOKEN, TELEGRAM_CHAT_ID
from habbits.models import Habit

bot_token = TELEGRAM_ACCESS_TOKEN
tg_chat_id = TELEGRAM_CHAT_ID
get_id_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'


def send_message_to_bot(chat_id, message):
    """ Функция отправки сообщения в телеграм-бот
    chat_id: id чата
    message: сообщение
    """

    params = {"chat_id": chat_id, "text": message}

    response = requests.get(send_message_url, params=params).json()

    return response


def create_massage(habit_id):

    habit = Habit.objects.get(id=habit_id)

    user = habit.habit_user
    habit_time = habit.habit_time
    action = habit.habit_action
    place = habit.habit_place
    duration = round(habit.habit_duration.total_seconds() / 60)

    message = f'Привет {user} ! Скоро надо сделать {action} в {habit_time} {place}. Надо успеть за {duration} минут'

    response = send_message_to_bot(tg_chat_id, message)

    if habit.connected_habit or habit.habit_prize:

        if habit.connected_habit:
            nice_habit_id = habit.connected_habit.id
            nice_habit = Habit.objects.get(id=nice_habit_id)

            nice_time = round(nice_habit.habit_duration.total_seconds() / 60)

            nice_message = (f'Если ты выработал полезную привычку, ты можешь {nice_habit.habit_action} '
                            f'в течение {nice_time} минут')

            time.sleep(10)
            nice_response = send_message_to_bot(tg_chat_id, nice_message)  # отправляем сообщение

            return HttpResponse(nice_response)

        if habit.habit_prize:
            prize_message = f'Если ты выработал полезную привычку, ты можешь {habit.habit_prize.prize_description}'

            time.sleep(10)
            nice_response = send_message_to_bot(tg_chat_id, prize_message)

            return HttpResponse(nice_response)

    return HttpResponse(response)


def get_bot_id():

    response = requests.get(get_id_url).json()

    return HttpResponse(response)
