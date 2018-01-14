from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.reverse import reverse
from api.models import TODOList, Task


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

class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=1)

    owner = serializers.PrimaryKeyRelatedField(queryset = TODOList.objects.all())

    deadline = serializers.DateTimeField()

    assigned_to = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), allow_null=True)

    def create(self, validated_data):
        task = Task.objects.create(title=validated_data['title'], deadline=validated_data['deadline'],
             owner=validated_data['owner'])
        return task

    class Meta:
        model = Task
        fields = ('id', 'title', 'deadline', 'owner', 'assigned_to')


class TODOListSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(min_length=1)

    owner = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())

    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = TODOList
        fields = ('url', 'title', 'owner', 'tasks')
        depth = 1
