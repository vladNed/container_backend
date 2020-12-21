from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

ContainerUser = get_user_model()


class ContainerUserSerializer(ModelSerializer):

    class Meta:
        model = ContainerUser
        fields = ('email', 'password', 'first_name', 'last_name', 'data_joined',
                  'last_login', 'role')

    def create(self, validated_data):
        return ContainerUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        return instance
