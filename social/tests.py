import pytest
from datetime import datetime
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt import exceptions

from social.models import User

USERNAME = "user1"
PASSWORD = "bar"
EMAIL = "user1@email.com"


@pytest.mark.django_db
def test_sign_up(client):
    response = client.post(
        '/api/users/',
        data={
            'username': USERNAME,
            'password': PASSWORD,
            'email': EMAIL,
        }
    )
    user = User.objects.filter(username=USERNAME).first()
    client.login(username=USERNAME, password=PASSWORD)

    assert response.status_code == 201
    assert user.email == EMAIL
    assert user.last_login
    assert 'tokens' in response.json()

    # invalid email
    response = client.post(
        '/api/users/',
        data={
            'username': 'new',
            'password': PASSWORD,
            'email': 'asfghd',
        }
    )
    assert response.status_code == 400

    # duplicated user
    response = client.post(
        '/api/users/',
        data={
            'username': USERNAME,
            'password': PASSWORD,
            'email': EMAIL,
        }
    )
    assert response.json() == {'username': ['A user with that username already exists.']}


@pytest.mark.django_db
def test_token_valid(client, create_user):
    # token is valid
    result = (
        authentication.JWTAuthentication().get_validated_token(
            create_user['tokens']['access']
            )
        )
    assert result

    # token is not valid
    pytest.raises(
        exceptions.InvalidToken, authentication.JWTAuthentication().get_validated_token,
        '123gkjhs'
    )


@pytest.mark.django_db
def test_get_users(client, create_user):
    response = client.get(
        '/api/users/',
        {},
        HTTP_AUTHORIZATION='Bearer {}'.format(create_user['tokens']['access']),
    )
    assert response.status_code == 200
    assert response.json()['count'] == 1

    # invalid token
    response = client.get(
        '/api/users/',
        {},
        HTTP_AUTHORIZATION='Bearer {}'.format('fake_token'),
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_posts(client, create_user):
    response = client.get(
        '/api/posts/',
        {},
        HTTP_AUTHORIZATION='Bearer {}'.format(create_user['tokens']['access']),
    )
    assert response.status_code == 200
    assert response.json()['count'] == 0


@pytest.mark.django_db
def test_create_post(client, create_user):
    # create a new post
    response = client.post(
        '/api/posts/',
        data={'text': 'smth interesting is here'},
        HTTP_AUTHORIZATION='Bearer {}'.format(create_user['tokens']['access']),
    )
    assert response.status_code == 201

    # get all posts and check amount
    response = client.get(
        '/api/posts/',
        {},
        HTTP_AUTHORIZATION='Bearer {}'.format(create_user['tokens']['access']),
    )
    assert response.json()['count'] == 1


@pytest.mark.django_db
def test_like_post(client, create_user, create_post):
    # like
    response = client.get(
        '/api/posts/1/toggle_like/',
        {},
        HTTP_AUTHORIZATION='Bearer {}'.format(create_user['tokens']['access']),
    )
    assert response.status_code == 200
    assert response.json()['likes_count'] == 1

    # unlike
    response = client.get(
        '/api/posts/1/toggle_like/',
        {},
        HTTP_AUTHORIZATION='Bearer {}'.format(create_user['tokens']['access']),
    )
    assert response.status_code == 200
    assert response.json()['likes_count'] == 0


@pytest.mark.django_db
def test_action(client, create_user, create_second_user, create_post_second_user):
    # check last action current user
    response = client.get(
        '/api/users/1/action/',
        {},
        HTTP_AUTHORIZATION='Bearer {}'.format(create_user['tokens']['access']),
    )
    assert response.json()['last_action'] == '/api/users/1/action/'
    assert 'last_login' in response.json()

    # check last action other user
    response = client.get(
        '/api/users/2/action/',
        {},
        HTTP_AUTHORIZATION='Bearer {}'.format(create_user['tokens']['access']),
    )
    assert response.json()['last_action'] == '/api/posts/'


@pytest.mark.django_db
def test_likes_analytics(client, create_user, create_post, like_post):
    str_today = datetime.strftime(datetime.today(), '%Y-%m-%d')

    # successful case
    response = client.get(
        '/api/analitics/?date_from={}&date_to={}'.format(str_today, str_today),
        {},
        HTTP_AUTHORIZATION='Bearer {}'.format(create_user['tokens']['access']),
    )
    assert response.status_code == 200
    assert response.json()['count'] == 1

    # unsuccessful cases
    response = client.get(
        '/api/analitics/?date_from={}&date_to='.format(str_today),
        {},
        HTTP_AUTHORIZATION='Bearer {}'.format(create_user['tokens']['access']),
    )
    assert response.status_code == 400

    response = client.get(
        '/api/analitics/?date_from=&date_to=',
        {},
        HTTP_AUTHORIZATION='Bearer {}'.format(create_user['tokens']['access']),
    )
    assert response.status_code == 400
