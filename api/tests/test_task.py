from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from api.services.tokens import account_activation_token
from datetime import datetime

class TaskTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        self.test_todo_list = self.test_user.todolist_set.create(title='Teste')

        self.client.force_authenticate(user=self.test_user)

    def test_create_task(self):
        data = {
            'title': 'Do todolist project',
            'deadline': datetime.strptime('16-01-2017', '%d-%m-%Y')
        }

        response = self.client.post(f'/api/todo/{self.test_todo_list.id}/tasks/', data, format='json')

        self.test_todo_list.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.test_todo_list.task_set.first().title, data['title'])
        self.assertEqual(self.test_todo_list.task_set.first().deadline.replace(tzinfo=None), data['deadline'])

