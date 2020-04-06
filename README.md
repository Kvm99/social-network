# Social Network simple REST API and bot

[![License: MIT](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

-------------
Simple API with the following features:
- user signup, login: `/api/users/`
- post creation: `/api/users/`
- post like, unlike: `/api/posts/22/toggle_like/`
- analytics about how many likes was made by each day. 
Example url: `/api/analitics/?date_from=2020-02-02&date_to=2020-02-15` 
- user activity an endpoint which will show when user was login last time and when he mades a last
request to the service.
Example url: `/api/users/33/action/` 

Bot-script with the following features:
- signup users (number provided in config, see bot_config.yaml)
- each user creates random number of posts with any content (up to
max_posts_per_user)
- After creating the signup and posting activity, posts will be liked randomly, posts
can be liked multiple times


## Usage
-------------
To use the Social Network simple REST API and bot you should:
* clone the repo
* install requirements: `pip3 install -r requirements.txt`
* run `python3 manage.py runserver`
* make requests to the API using [Postman](https://www.postman.com/) or requests library
* run `bot.py`, add values to `bot_config.yaml` 


## Tests
-----
To run tests you should run `pytest`

## Contributing
-------------
As I use this for my own projects, I know this might not be the perfect approach for all the projects out there.
If you have any ideas, just open an issue and tell me what you think.

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.


## Licensing
-------------
This project is licensed under BSD-3 license.
This license allows unlimited redistribution for any purpose as long as its copyright notices and the license's disclaimers of warranty are maintained.

## Contacts
-------------
Facebook: <https://www.facebook.com/maria.kuznetsova.1048>

Email: <mary@filonova.dev>
