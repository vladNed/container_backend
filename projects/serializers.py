from rest_framework import serializers
from projects.models import ProjectUser, Project


class ProjectUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectUser
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    users = ProjectUserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'start_date', 'end_date', 'users')
