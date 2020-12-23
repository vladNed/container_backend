from rest_framework import viewsets
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from projects.models import Project, ProjectUser

from projects.serializers import ProjectSerializer, ProjectUserSerializer

from django.db.utils import IntegrityError


class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser, ]

    def retrieve(self, request, pk=None):
        project = self.get_object()
        return Response(
            ProjectSerializer(project).data,
            status=status.HTTP_200_OK
        )

    def update(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(dict(
            detail=serializer.data
        ), status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.create(serializer.data)
            except IntegrityError:
                raise ParseError

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        project = self.get_object()
        try:
            project.delete()
        except Exception as ex:
            raise ParseError(f'Error occured while deleting project: {str(ex)}')

        return Response(dict(
            detail=f"Project `{project.name}` was removed"
        ), status=status.HTTP_204_NO_CONTENT)


class ProjectUserViewSet(viewsets.ModelViewSet):

    queryset = ProjectUser.objects.all()
    serializer_class = ProjectUserSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]
