from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.serializers import TODOListSerializer
from api.models import TODOList


class TODOListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = TODOListSerializer

    def get_queryset(self):
        user = self.request.user
        return TODOList.objects.filter(owner=self.request.user).order_by('created_at')

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        return super(self.__class__, self).create(request, *args, **kwargs)

