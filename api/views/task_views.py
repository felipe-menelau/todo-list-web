from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.serializers import UserSerializer, TODOListSerializer, TaskSerializer
from api.services.tokens import account_activation_token
from api.models import TODOList, Task

class TaskCreation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format='json'):
        request.data['owner'] = pk
        serializer_context = {
                'request': request,
                }

        serializer = TaskSerializer(data=request.data, context=serializer_context)

        if serializer.is_valid():
            task = serializer.save()
            task.save()
            if task:
                return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format='json'):
        try:
            queryset = TODOList.objects.get(owner=request.user.id, id=pk).task_set.all()
        except(TypeError, ValueError, OverflowError, TODOList.DoesNotExist):
            return Response('', status.HTTP_400_BAD_REQUEST)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class TaskManagement(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, pk_task, format='json'):
        try:
            task = Task.objects.get(owner=request.user.pk, id=pk_task)
        except(TypeError, ValueError, OverflowError, Task.DoesNotExist):
            task = None
        if task is not None:
            request.data['owner'] = task.owner.id
            if 'title' not in request.data:
                request.data['title'] = task.title
            if 'deadline' not in request.data:
                request.data['deadline'] = task.deadline

            if 'assigned_to' not in request.data:
                request.data['assigned_to'] = task.assigned_to
            else:
                try:
                    request.data['assigned_to'] = User.objects.get(username=request.data['assigned_to']).id
                except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                    return Response('invalid username', status.HTTP_400_BAD_REQUEST)

            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response('', status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, pk_task, format='json'):
        try:
            task = Task.objects.get(owner=pk, id=pk_task)
        except(TypeError, ValueError, OverflowError, Task.DoesNotExist):
            return Response('', status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response('', status.HTTP_204_NO_CONTENT)
