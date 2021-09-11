from rest_framework import status
from rest_framework.test import APITestCase
from blog.models import User
from tests.conftest import URL

class UserTests(APITestCase):
    def test_check_user(self):
        route = '/api/user/'
        user = User.objects.create_user('medical', 'Pas$w0rd')
        self.client.force_authenticate(user)
        response = self.client.get(URL + route)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_1(self):
        route = '/api/user/'
        data = {
            'username': 'Test',
        }
        response = self.client.post(URL + route, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_2(self):
        user = User.objects.create_user('Test', 'Pas$w0rd')
        user.save()
        user.refresh_from_db()
        # self.client.login(username='Test', password='Pas$w0rd')
        self.client.force_authenticate(user)

        route = '/api/user/'
        data = {
            'id': 1,
            'username': 'Vampire',
        }

        response = self.client.post(URL + route, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(User.objects.get(username='Vampire').username, 'Vampire')