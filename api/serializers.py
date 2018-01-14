from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.models import TODOList


class UserSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())])

    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())])

    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password')

class TODOListSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(min_length=1)

    owner = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())

    class Meta:
        model = TODOList
        fields = ('url', 'title', 'owner')
        depth = 1
