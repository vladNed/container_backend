from datetime import date
from django.db import models

from users.models import ContainerUser


class Project(models.Model):
    '''
    Project base class
    '''

    name = models.CharField(max_length=100, unique=True, null=False)
    start_date = models.DateField(auto_now_add=True, null=False)
    end_date = models.DateField(null=False)

    class Meta:
        ordering = ['-start_date']

    def __str__(self) -> str:
        return f'[{self.pk}] {self.name} - {self.start_date}'

    def days_left(self) -> int:
        if date.today() > self.end_date:
            return 0
        date_result = self.end_date - date.today()

        return date_result.days


class ProjectUser(models.Model):
    '''
    Table to keep all the users related to a project
    '''

    user = models.ForeignKey(
        ContainerUser,
        on_delete=models.CASCADE,
        null=False,
        related_name='projects'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=False,
        related_name='users'
    )

    class Meta:
        unique_together = ['user', 'project']

    def __str__(self) -> str:
        return f'User: `{self.user}` -> Project: {self.project}'
