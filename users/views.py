from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView
)
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND
)
from users.models import ContainerUser
from users.serializers import ContainerUserSerializer
from rest_framework.exceptions import NotFound


class ContainerUserList(ListAPIView):
    '''
    Returns the list of users
    Note: Only accessible by admin users
    '''

    queryset = ContainerUser.objects.all()
    serializer_class = ContainerUserSerializer
    authentication_classes = [BasicAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser, ]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ContainerUserSerializer(queryset, many=True)
        data = self.__remove_password_field(serializer.data)

        return Response(dict(
            profiles=data
        ), status=HTTP_200_OK)

    @staticmethod
    def __remove_password_field(queryset):
        for user in queryset:
            user.pop('password')

        return queryset


class ContainerUserCreate(CreateAPIView):
    '''
    Creates a new account
    Note: Only accessible by admin users
    '''

    authentication_classes = [BasicAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser, ]

    def create(self, request):
        user_data = request.data
        serializer = ContainerUserSerializer(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.data)

        return Response(dict(
            details='User created'
        ), status=HTTP_201_CREATED)


class ContainerUserUpdate(UpdateAPIView):
    '''
    Update a user profile
    '''

    serializer_class = ContainerUserSerializer
    authentication_classes = [BasicAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def _get_user_by_pk(self, user_pk: int) -> ContainerUser:
        try:
            user_object = ContainerUser.objects.get(pk=user_pk)
        except ContainerUser.DoesNotExist:
            raise NotFound

        return user_object

    def partial_update(self, request, pk=None):
        if pk is None:
            user = self._get_object_by_pk(request.user.pk)
        else:
            user = self._get_object_by_pk(pk)

        serializer = ContainerUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(dict(
            message='Profile updated',
            profile=str(user)
        ), status=HTTP_200_OK)


class ContainerUserRetrieve(RetrieveAPIView):
    '''
    Retrieves user profile
    '''

    authentication_classes = [BasicAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def _get_user_by_pk(self, user_pk: int) -> ContainerUser:
        try:
            user_object = ContainerUser.objects.get(pk=user_pk)
        except ContainerUser.DoesNotExist:
            raise NotFound

        return user_object

    def retrieve(self, request, pk=None):
        user_obj = self._get_user_by_pk(pk)
        serializer = ContainerUserSerializer(user_obj)
        if serializer.is_valid(raise_exception=True):
            user = serializer.data
            user.pop('password')

        return Response(dict(
            profile=user
        ), status=HTTP_200_OK)


class ContainerUserDestroy(DestroyAPIView):
    '''
    Deletes a user profile
    Note: Only accesible by an admin user
    '''

    authentication_classes = [BasicAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def _get_user_by_pk(self, user_pk: int) -> ContainerUser:
        try:
            user_object = ContainerUser.objects.get(pk=user_pk)
        except ContainerUser.DoesNotExist:
            raise NotFound

        return user_object

    def destroy(self, request, pk=None):
        user_obj = self._get_user_by_pk(pk)
        try:
            user_obj.delete()
        except Exception as ex:
            return Response(dict(
                details=f'Could not delete user: {repr(ex)}'
            ), status=HTTP_404_NOT_FOUND)

        return Response(dict(
            details='User deleted',
            profile=str(user_obj)
        ), status=HTTP_204_NO_CONTENT)
