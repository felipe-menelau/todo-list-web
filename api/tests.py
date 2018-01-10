from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status

class UserTest(APITestCase):
    def set_up(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        self.create_url = reverse('user-create')

    def test_create_user(self):
        data = {
            'username': 'CarlosDoTeste',
            'email': 'carlos@email.com',
            'password': 'carlosdemais123'
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(User.objects().count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)
