from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class UserCreate(APIView):
    def post(self, request, format='json'):
        serializer_context = {
                'request': request,
                }

        serializer = UserSerializer(data=request.data, context=serializer_context)

        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status.HTTP_201_CREATED)
