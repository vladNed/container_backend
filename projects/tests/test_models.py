from datetime import date
from datetime import timedelta

import pytest

from projects.models import Project, ProjectUser
from users.models import ContainerUser

from django.db.utils import IntegrityError

pytestmark = pytest.mark.django_db

# FIXUTRES ------


@pytest.fixture
def container_user() -> ContainerUser:
    return ContainerUser.objects.create_user(
        email="testuser1@email.com",
        password="TestPassword111",
        role="PR"
    )


@pytest.fixture
def test_project() -> Project:
    return Project.objects.create(
        name="Test project 1",
        end_date=date.today() + timedelta(days=2),
    )


@pytest.fixture
def test_projects() -> Project:
    projects = []
    project1 = Project.objects.create(
        name="Test project 1",
        end_date=date.today() + timedelta(days=2),
    )
    project2 = Project.objects.create(
        name="Test project 2",
        end_date=date.today() + timedelta(days=2),
    )
    projects.append(project1)
    projects.append(project2)

    return projects

# TESTS ------


def test_create_project():
    project = Project.objects.create(
        name="Test project 1",
        end_date=date.today() + timedelta(days=2),
    )

    assert Project.objects.count() == 1
    assert project.days_left() == 2


def test_no_days_left():
    project = Project.objects.create(
        name="Test project 1",
        start_date=date.today() - timedelta(days=2),
        end_date=date.today() - timedelta(days=1)
    )

    assert Project.objects.count() == 1
    assert project.days_left() == 0


def test_project_user_create(container_user, test_project):
    ProjectUser.objects.create(
        user=container_user,
        project=test_project
    )

    assert ProjectUser.objects.count() == 1


def test_project_creating_same_project_user(container_user, test_projects):
    with pytest.raises(IntegrityError):
        ProjectUser.objects.create(
            user=container_user,
            project=test_projects[0]
        )

        ProjectUser.objects.create(
            user=container_user,
            project=test_projects[0]
        )
