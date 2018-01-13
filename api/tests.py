from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class UserTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        self.create_url = reverse('user-create')
        self.activate_url = reverse('user-activate')

    def test_create_user(self):
        data = {
            'username': 'CarlosDoTeste',
            'email': 'carlos@email.com',
            'password': 'carlosdemais123'
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)
        self.assertFalse(User.objects.get(username=data['username']).is_active, False)

    def test_activate_user(self):
        from api.tokens import account_activation_token

        just_registered_user = User.objects.create_user('carlos', 'carlos@example.com', 'carlospassword')
        just_registered_user.is_active = False
        just_registered_user.save()

        just_registered_uid = urlsafe_base64_encode(force_bytes(just_registered_user.pk))
        just_registered_token = account_activation_token.make_token(just_registered_user)

        data = {
            'uid': just_registered_uid,
            'token': just_registered_token
        }

        response = self.client.patch(self.activate_url, data, format='json')

        just_registered_user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(just_registered_user.is_active, True)

    def test_forgot_password(self):
        forgetful_user = User.objects.create_user('rodrigo', 'rodrigo@exemple.com', 'forgottenpassword')

        data = {
            'email': forgetful_user.email
        }

        response = self.client.post(self.forgot_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
