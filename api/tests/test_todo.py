from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from api.services.tokens import account_activation_token
from datetime import datetime

class TODOListTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        self.todo_create_url = '/api/todo/'

        self.client.force_authenticate(user=self.test_user)

    def test_create_todo_list(self):
        data = {
            'title': 'List',
        }

        response = self.client.post(self.todo_create_url, data, format='json')

        self.test_user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.test_user.todolist_set.first().title, data['title'])

    def test_delete_todo_list(self):
        todo_to_delete = self.test_user.todolist_set.create(title='Teste')

        response = self.client.delete(f'/api/todo/{todo_to_delete.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_edit_todo_list(self):
        todo_to_edit = self.test_user.todolist_set.create(title='Teste')

        data = {
            'title': 'New name',
        }

        response = self.client.patch(f'/api/todo/{todo_to_edit.id}/', data, format='json')

        todo_to_edit.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(todo_to_edit.title, data['title'])
