from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habbits.models import Habit, Prize
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(user_email='titadarenka@gmail.com')
        self.user.set_password('dasha888')
        self.user.save()

        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """ Тест на создание привычки """

        response = self.client.post('/users/token/', {"user_email": "titadarenka@gmail.com", "password": "dasha888"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        data_habit = {
            'habit_user': 'Test',
            'habit_name': 'Test',
            'habit_action': 'Test',
            'habit_is_nice': True,
            'habit_period': 'ежедневно',
            'habit_owner': self.user.pk
        }

        response = self.client.post(
            '/habits/habit_create/',
            data=data_habit
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            response.json(),
            {'id': 2, 'habit_user': 'Test', 'habit_name': 'Test', 'habit_place': None, 'habit_time': None,
             'habit_action': 'Test', 'habit_is_nice': True, 'habit_period': 'ежедневно', 'habit_duration': '00:02:00',
             'habit_is_public': False, 'connected_habit': None, 'habit_prize': None, 'habit_owner': 2}
        )

        self.assertTrue(
            Habit.objects.all().exists()
        )

    def test_list_habit(self):
        """ Тест получения списка привычек """

        response = self.client.post('/users/token/', {"user_email": "titadarenka@gmail.com", "password": "dasha888"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        Habit.objects.create(
            habit_user='Test',
            habit_name='Test',
            habit_action='Test',
            habit_is_nice=True,
            habit_period='ежедневно',
            habit_owner=self.user
        )

        response = self.client.get(
            '/habits/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [{'id': 5, 'habit_user': 'Test',
                                                                      'habit_name': 'Test', 'habit_place': None,
                                                                      'habit_time': None, 'habit_action': 'Test',
                                                                      'habit_is_nice': True,
                                                                      'habit_period': 'ежедневно',
                                                                      'habit_duration': '00:02:00',
                                                                      'habit_is_public': True, 'connected_habit': None,
                                                                      'habit_prize': None, 'habit_owner': 5}]}

        )

    def test_detail_habit(self):
        """ Тест на получение информации о привычке """

        response = self.client.post('/users/token/', {"user_email": "titadarenka@gmail.com", "password": "dasha888"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        habit = Habit.objects.create(
            habit_user='Test',
            habit_name='Test',
            habit_action='Test',
            habit_is_nice=True,
            habit_period='ежедневно',
            habit_owner=self.user
        )

        response = self.client.get(
            reverse('habits:habit_detail', kwargs={'pk': habit.pk})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'id': 4, 'habit_user': 'Test', 'habit_name': 'Test', 'habit_place': None, 'habit_time': None,
             'habit_action': 'Test', 'habit_is_nice': True, 'habit_period': 'ежедневно', 'habit_duration': '00:02:00',
             'habit_is_public': True, 'connected_habit': None, 'habit_prize': None, 'habit_owner': 4}
        )

    def test_change_habit(self):
        """ Тест изменения привычки """

        response = self.client.post('/users/token/', {"user_email": "titadarenka@gmail.com", "password": "dasha888"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        habit = Habit.objects.create(
            habit_user='Test',
            habit_name='Test',
            habit_action='Test',
            habit_is_nice=True,
            habit_period='ежедневно',
            habit_owner=self.user
        )

        data_habit_change = {
            'habit_user': 'Test_1',
        }

        response = self.client.patch(
            reverse('habits:habit_change', kwargs={'pk': habit.pk}),
            data=data_habit_change
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'id': 1, 'habit_user': 'Test_1', 'habit_name': 'Test', 'habit_place': None, 'habit_time': None,
             'habit_action': 'Test', 'habit_is_nice': True, 'habit_period': 'ежедневно', 'habit_duration': '00:02:00',
             'habit_is_public': True, 'connected_habit': None, 'habit_prize': None, 'habit_owner': 1}
        )

    def test_delete_habit(self):
        """ Тест на удаление привычки """

        response = self.client.post('/users/token/', {"user_email": "titadarenka@gmail.com", "password": "dasha888"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        habit = Habit.objects.create(
            habit_user='Test',
            habit_name='Test',
            habit_action='Test',
            habit_is_nice=True,
            habit_period='ежедневно',
            habit_owner=self.user
        )

        response = self.client.delete(
            reverse('habits:habit_delete', kwargs={'pk': habit.pk})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class PrizeTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(user_email='titadarenka@gmail.com')
        self.user.set_password('dasha888')
        self.user.save()

        self.client.force_authenticate(user=self.user)

    def test_create_prize(self):
        """ Тест на создание награды """

        response = self.client.post('/users/token/', {"user_email": "titadarenka@gmail.com", "password": "dasha888"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        data_prize = {
            'prize_name': 'Test',
            'prize_description': 'Test',
            'prize_owner': self.user.pk
        }

        response = self.client.post(
            '/habits/prize_create/',
            data=data_prize
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            response.json(),
            {'id': 2, 'prize_name': 'Test', 'prize_description': 'Test', 'prize_owner': 7}
        )

        self.assertTrue(
            Prize.objects.all().exists()
        )

    def test_list_prize(self):
        """ Тест на получение списка наград """

        response = self.client.post('/users/token/', {"user_email": "titadarenka@gmail.com", "password": "dasha888"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        Prize.objects.create(
            prize_name='Test',
            prize_description='Test',
            prize_owner=self.user
        )

        response = self.client.get(
            '/habits/prizes/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [{'id': 5, 'prize_name': 'Test',
                                                                      'prize_description': 'Test', 'prize_owner': 10}]}
        )

    def test_detail_prize(self):
        """ Тест на информацию о награде """

        response = self.client.post('/users/token/', {"user_email": "titadarenka@gmail.com", "password": "dasha888"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        prize = Prize.objects.create(
            prize_name='Test',
            prize_description='Test',
            prize_owner=self.user
        )

        response = self.client.get(
            reverse('habits:prize_detail', kwargs={'pk': prize.pk})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'id': 4, 'prize_name': 'Test', 'prize_description': 'Test', 'prize_owner': 9}
        )

    def test_change_prize(self):
        """ Тест на изменение награды """

        response = self.client.post('/users/token/', {"user_email": "titadarenka@gmail.com", "password": "dasha888"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        prize = Prize.objects.create(
            prize_name='Test',
            prize_description='Test',
            prize_owner=self.user
        )

        data_prize_change = {
            'prize_name': 'Test_1',
        }

        response = self.client.patch(
            reverse('habits:prize_change', kwargs={'pk': prize.pk}),
            data=data_prize_change
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'id': 1, 'prize_name': 'Test_1', 'prize_description': 'Test', 'prize_owner': 6}
        )

    def test_delete_prize(self):
        """ Тест на удаление награды """

        response = self.client.post('/users/token/', {"user_email": "titadarenka@gmail.com", "password": "dasha888"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        prize = Prize.objects.create(
            prize_name='Test',
            prize_description='Test',
            prize_owner=self.user
        )

        response = self.client.delete(
            reverse('habits:prize_delete', kwargs={'pk': prize.pk})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
