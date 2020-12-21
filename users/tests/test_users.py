import pytest

from users.models.user import ContainerUser
from users.models.constants import Roles

pytestmark = pytest.mark.django_db


def test_user_create():
    ContainerUser.objects.create_user(
        email='some_user@email.com',
        password='TestPassword123',
        first_name='John',
        last_name='Doe',
        role=Roles.PROCESSOR
    )

    assert ContainerUser.objects.count() == 1


def test_user_create_fail():
    with pytest.raises(ValueError):
        ContainerUser.objects.create_user(
            email=None,
            password=None
        )


def test_create_super_user():
    superuser = ContainerUser.objects.create_superuser(
        email="admin@email.com",
        password="TestPassword123",
    )

    assert superuser.is_superuser is True
    assert superuser.is_active is True
    assert superuser.is_staff is True
    assert superuser.is_admin is True


def test_retrieve_user():
    user = ContainerUser.objects.create_user(
        email='some_user@email.com',
        password='TestPassword123',
        first_name='John',
        last_name='Doe',
        role=Roles.PROCESSOR
    )

    user_a = ContainerUser.objects.get(instance=user)

    assert user_a is not None
