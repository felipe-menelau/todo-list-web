from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.serializers import UserSerializer, TODOListSerializer, TaskSerializer
from api.mail_sender import send_confirmation_email, send_forgot_password_email
from api.tokens import account_activation_token
from api.models import TODOList

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

class TaskManagement(APIView):
    permission_classes = [IsAuthenticated]

