from django.contrib.auth import get_user_model
from rest_framework import serializers

from projects.serializers import ProjectUserSerializer

ContainerUser = get_user_model()


class ContainerUserSerializer(serializers.ModelSerializer):
    projects = ProjectUserSerializer(many=True, read_only=True)

    class Meta:
        model = ContainerUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'data_joined', 'is_active',
                  'role', 'projects')

    def create(self, validated_data):
        return ContainerUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        return instance
