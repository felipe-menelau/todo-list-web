from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.serializers import UserSerializer, TODOListSerializer, TaskSerializer
from api.services.mail_sender import send_confirmation_email, send_forgot_password_email
from api.services.tokens import account_activation_token
from api.models import TODOList

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

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
            user.is_active = False
            send_confirmation_email(user)
            user.save()
            if user:
                return Response(serializer.data, status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class UserActivate(APIView):
    def patch(self, request, format='json'):
        uid = force_text(urlsafe_base64_decode(request.data['uid']))
        token = request.data['token']
        try:
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response('success', status.HTTP_200_OK)
        else:
            return Response('failed', status.HTTP_401_UNAUTHORIZED)

class UserPasswordManagement(APIView):
    def post(self, request, format='json'):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None:
            send_forgot_password_email(user)
            return Response('', status.HTTP_204_NO_CONTENT)
        else:
            return Response('', status.HTTP_204_NO_CONTENT)

    def patch(self, request, format='json'):
        uid = force_text(urlsafe_base64_decode(request.data['uid']))
        token = request.data['token']
        try:
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.set_password(request.data['new_password'])
            user.save()
            return Response('success', status.HTTP_202_ACCEPTED)
        else:
            return Response('', status.HTTP_400_BAD_REQUEST)

