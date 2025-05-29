from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Habits

User = get_user_model()

class HabitsCreate(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="sample@example.ru")
        self.habits_1 = Habits.objects.create(
            owner=self.user,
            place="Кухня",
            time="10:00",
            move="Попить кофе",
            good_hab=False,
            periodicity=1,
            execution_time="00:02:00",
            is_public=False,
            last_remember=None
        )
        self.habits_2 = Habits.objects.create(
            owner=self.user,
            place="Спальня",
            time="10:05",
            move="Отжимания",
            good_hab=True,
            linked_hab= self.habits_1,
            periodicity=1,
            #reward="Конфета",
            execution_time="00:02:00",
            is_public=True,
            last_remember=None
        )
        self.client.force_authenticate(user=self.user)


    def test_habits_list_public(self):
        url = reverse('habbits:public-habits-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data,
            [{'id': 2, 'place': 'Спальня', 'time': '10:05:00', 'move': 'Отжимания', 'periodicity': 1, 'execution_time': '00:02:00'}]
        )

    def test_habits_validation(self):
        url = reverse('habbits:habits_create')
        data = {
            "place": "",
            "time": "25:00:00",
            "move": "",
            "good_hab": False,
            "periodicity": 8,
            "reward": "Конфета",
            "execution_time": "00:10:00",
            "is_public": True,
            "last_remember": None
        }

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_data = response.data
        self.assertEqual(str(error_data['place'][0]), "This field may not be blank.")
        self.assertEqual(str(error_data['time'][0]), "Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]].")
        self.assertEqual(str(error_data['execution_time'][0]), "Ensure this value is less than or equal to 0:02:00.")



