from urllib.parse import urljoin

import requests

BASE_URL = 'http://localhost:8000'


def test_login_pass():
    with requests.Session() as s:
        user = {'name': 'tota', 'password': 'password123'}
        response = s.post(urljoin(BASE_URL, '/session/new'), data=user, allow_redirects=False)
        assert response.status_code == 302

        response = s.get(urljoin(BASE_URL, '/'))
        assert user['name'] in response.text


def test_wrong_login():
    with requests.Session() as s:
        user = {'name': 'wrong', 'password': 'password123'}
        response = s.post(urljoin(BASE_URL, '/session/new'), data=user, allow_redirects=False)

        response = s.get(urljoin(BASE_URL, '/'))
        assert 'Wrong' in response.text


def test_wrong_password():
    with requests.Session() as s:
        user = {'name': 'tota', 'password': 'wrong'}
        response = s.post(urljoin(BASE_URL, '/session/new'), data=user, allow_redirects=False)

        response = s.get(urljoin(BASE_URL, '/'))
        assert 'Wrong' in response.text


def test_post_session():
    with requests.Session() as s:
        user = {'name': 'tota', 'password': 'password123'}
        response = s.post(urljoin(BASE_URL, '/session/new'), data=user, allow_redirects=False)

        response = s.post(urljoin(BASE_URL, '/session/delete'), allow_redirects=False)
        response = s.get(urljoin(BASE_URL, '/'))
        assert user['name'] not in response.text


def test_delete_session():
    with requests.Session() as s:
        user = {'name': 'tota', 'password': 'password123'}
        response = s.post(urljoin(BASE_URL, '/session/new'), data=user, allow_redirects=False)

        response = s.delete(urljoin(BASE_URL, '/session/delete'), allow_redirects=False)
        response = s.get(urljoin(BASE_URL, '/'))
        assert user['name'] not in response.text
