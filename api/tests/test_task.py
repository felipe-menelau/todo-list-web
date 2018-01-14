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

        self.test_task = self.test_todo_list.task_set.create(title='Do things', deadline=datetime.strptime('16-01-2017', '%d-%m-%Y'))

        self.client.force_authenticate(user=self.test_user)

    def test_create_task(self):
        data = {
            'title': 'Do todolist project',
            'deadline': datetime.strptime('16-01-2017', '%d-%m-%Y'),
            'assigned_to': None
        }

        response = self.client.post(f'/api/todo/{self.test_todo_list.id}/tasks/', data, format='json')

        self.test_todo_list.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.test_todo_list.task_set.get(title=data['title']).title, data['title'])
        self.assertEqual(self.test_todo_list.task_set.get(title=data['title']).deadline.replace(tzinfo=None), data['deadline'])

    def test_list_all_tasks(self):
        self.test_todo_list.task_set.create(title='Taskerino', deadline=datetime.strptime('16-01-2017', '%d-%m-%Y'), assigned_to=None)

        response = self.client.get(f'/api/todo/{self.test_todo_list.id}/tasks/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_edit_task_name(self):
        data = {
            'title': 'Do meanignful things',
        }

        current_title = self.test_task.title
        current_deadline = self.test_task.deadline

        response = self.client.patch(
                reverse('task-detail', kwargs={'pk': self.test_todo_list.id, 'pk_task': self.test_task.id}),
                data,
                format='json'
            )

        self.test_task.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
