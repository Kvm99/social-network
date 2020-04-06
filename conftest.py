import pytest


@pytest.fixture
def create_user(client):
    response = client.post(
        '/api/users/',
        data={
            'username': "user1",
            'password': "bar",
            'email': "user@mail.ru",
        }
    )
    return response.json()


@pytest.fixture
def create_second_user(client):
    response = client.post(
        '/api/users/',
        data={
            'username': "user2",
            'password': "bar2",
            'email': "user2@mail.ru",
        }
    )
    return response.json()


@pytest.fixture
def create_post(client, create_user):
    response = client.post(
        '/api/posts/',
        data={'text': 'smth interesting is here'},
        HTTP_AUTHORIZATION='Bearer {}'.format(create_user['tokens']['access']),
    )
    return response


@pytest.fixture
def create_post_second_user(client, create_second_user):
    response = client.post(
        '/api/posts/',
        data={'text': 'smth interesting is here'},
        HTTP_AUTHORIZATION='Bearer {}'.format(create_second_user['tokens']['access']),
    )
    return response


@pytest.fixture
def like_post(client, create_user):
    response = client.get(
        '/api/posts/1/toggle_like/',
        {},
        HTTP_AUTHORIZATION='Bearer {}'.format(create_user['tokens']['access']),
    )
    return response
