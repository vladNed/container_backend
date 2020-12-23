import pytest
from django.urls import reverse
from users.models import ContainerUser

pytestmark = pytest.mark.django_db

# FIXTURES -----------


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
def refresh_token(authenticated_admin, admin_user):
    data = {
        'email': admin_user.email,
        'password': 'TestPassword123'
    }

    response = authenticated_admin.post(
        path=reverse('token-pair'),
        data=data,
        format='json'
    )

    return response.json().get('refresh', None)


@pytest.fixture
def container_user() -> ContainerUser:
    '''
    Create a container user
    '''
    return ContainerUser.objects.create_user(
        email='randomuser@email.com',
        password="TestPassword123",
        first_name="John",
        last_name="Doe",
        role='PR'
    )


@pytest.fixture
def authenticated_admin(api_client, admin_user: ContainerUser):
    api_client.force_authenticate(user=admin_user)
    yield api_client


@pytest.fixture
def authenticated_user(api_client, container_user: ContainerUser):
    api_client.force_authenticate(user=container_user)
    yield api_client


@pytest.fixture
def random_user(api_client):
    api_client.force_authenticate(user=None)
    yield api_client

# USERS TESTS -----------


def test_list_authenticated(authenticated_admin):
    response = authenticated_admin.get(reverse('users:users-list'))

    assert response.status_code == 200
    assert len(response.json().get('profiles')) == 1


def test_list_not_authenticated(random_user):
    response = random_user.get(reverse('users:users-list'))

    assert response.status_code == 401
    assert 'profiles' not in response.json()


def test_create_user(authenticated_admin):
    data = {
        'email': 'newuser@email.com',
        'password': 'TestPassword123',
        'first_name': 'John',
        'last_name': 'Doe',
        'role': 'PR'
    }

    response = authenticated_admin.post(reverse('users:users-create'), data=data)

    assert response.status_code == 201
    assert response.json().get('detail') is not None


def test_create_user_not_all_fields(authenticated_admin):
    data = {
        'email': 'newuser@email.com',
        'password': 'TestPassword123',
        'first_name': 'John',
        'last_name': 'Doe',
    }

    response = authenticated_admin.post(reverse('users:users-create'), data=data)

    assert response.status_code == 400
    assert response.json().get('detail') == 'Not all fields were correctly given'


def test_update_admin_user(authenticated_admin, admin_user):
    data = {
        'first_name': 'Vlad'
    }

    response = authenticated_admin.patch(reverse('users:user-update'), data=data)
    user = ContainerUser.objects.get(pk=admin_user.pk)

    assert response.status_code == 200
    assert response.json().get('message') == 'Profile updated'
    assert response.json().get('profile') == str(user)
    assert user.first_name == 'Vlad'


def test_update_random_user(authenticated_user, container_user):
    data = {
        'first_name': 'John',
    }

    response = authenticated_user.patch(reverse('users:user-update'), data=data)
    user = ContainerUser.objects.get(pk=container_user.pk)

    assert response.status_code == 200
    assert response.json().get('message') == 'Profile updated'
    assert response.json().get('profile') == str(user)
    assert user.first_name == 'John'
