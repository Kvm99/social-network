import requests
import random
import yaml
from faker import Faker


with open('bot_config.yaml') as f:
    MAX_VALUES = yaml.load(f, Loader=yaml.FullLoader)
    API_URL = MAX_VALUES['api_url']

REFRESH_TOKEN_URL = '{}{}'.format(API_URL, 'api/token/refresh/')
USERS_URL = '{}{}'.format(API_URL, 'api/users/')
POSTS_URL = '{}{}'.format(API_URL, 'api/posts/')


def make_request(method, url, user=None, **kwargs):
    response = requests.request(method, url, **kwargs)

    if response.status_code == 401 and user is not None:
        user = refresh_token(user)
        return make_request(method, url, user, **kwargs)

    return response.json()


def refresh_token(user):
    payload = {
        'Content-type': 'application/json',
        'refresh': '{}'.format(user['tokens']['refresh'])
    }
    response = requests.post(REFRESH_TOKEN_URL, payload)
    user['tokens']['access'] = response.json()['access']

    return user


def get_posts(user):
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(user['tokens']['access'])
    }
    response = requests.get(POSTS_URL, headers=headers)

    return response.json()


def take_random_post(posts):
    random_post = random.choice(posts)
    return random_post


def generate_user(fake):
    user = {}
    user['email'] = fake.email()
    user['username'] = fake.profile()["username"]
    user['password'] = fake.password()

    return user


if __name__ == "__main__":
    fake = Faker()

    # create users
    for number in range(0, MAX_VALUES['number_of_users']):
        user = generate_user(fake)
        logged_user = make_request(
            'POST',
            USERS_URL,
            data={
                'username': user['username'],
                'email': user['email'],
                'password': user['password']
            }
        )

        # create posts
        for number in range(0, MAX_VALUES['max_posts_per_user']):
            make_request(
                'POST',
                POSTS_URL,
                headers={
                    'Content-type': 'application/json',
                    'Authorization': 'Bearer {}'.format(logged_user['tokens']['access'])
                },
                json={
                    'text': fake.pystr()
                }
            )

        all_posts = get_posts(logged_user)

        # like random posts
        for number in range(0, MAX_VALUES['max_likes_per_user']):
            random_post = take_random_post(all_posts['results'])

            make_request(
                'GET',
                '{}{}'.format(random_post['url'], 'toggle_like/'),
                logged_user,
                headers={
                    'Content-type': 'application/json',
                    'Authorization': 'Bearer {}'.format(logged_user['tokens']['access'])
                },
            )
