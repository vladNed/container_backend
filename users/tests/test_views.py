import pytest
from django.urls import reverse
from users.models import ContainerUser

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def admin_user() -> ContainerUser:
    '''
    Create an admin user
    '''
    return ContainerUser.objects.create_superuser(
        email="adminUser@email.com",
        password="TestPassword123",
        first_name="John",
        last_name="Doe"
    )


@pytest.fixture
def authenticated_admin(api_client, admin_user: ContainerUser):
    api_client.force_authenticate(user=admin_user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def random_user(api_client):
    api_client.force_authenticate(user=None)
    yield api_client


def test_list_authenticated(authenticated_admin):
    response = authenticated_admin.get(reverse('users-list'))

    assert response.status_code == 200
    assert len(response.json().get('profiles')) == 1


def test_list_not_authenticated(random_user):
    response = random_user.get(reverse('users-list'))

    assert response.status_code == 401
    assert 'profiles' not in response.json()
