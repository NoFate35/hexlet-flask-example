from urllib.parse import urljoin

import requests

BASE_URL = 'http://localhost:8000'


def test_create_post():
    with requests.Session() as s:
        data = {'title': 'first', 'body': 'first_body'}
        response = s.post(urljoin(BASE_URL, '/posts'), data=data, allow_redirects=False)
        assert response.status_code == 302

        response = s.get(urljoin(BASE_URL, '/posts'))
        assert data['title'] in response.text


def test_update_post():
    with requests.Session() as s:
        data = {'title': 'first', 'body': 'first_body'}
        response = s.post(urljoin(BASE_URL, '/posts'), data=data, allow_redirects=False)
        id = response.headers['X-ID']
        assert response.status_code == 302

        response = s.get(urljoin(BASE_URL, f'/posts/{id}/update'))
        assert data['title'] in response.text
        assert data['body'] in response.text

        post_data = {'title': 'post', 'body': 'post_body'}
        response = s.post(urljoin(BASE_URL, f'/posts/{id}/update'), data=post_data, allow_redirects=False)

        response = s.get(urljoin(BASE_URL, '/posts'))
        assert data['title'] not in response.text
        assert post_data['title'] in response.text


def test_update_with_errors():
    with requests.Session() as s:
        data = {'title': 'first', 'body': 'first_body'}
        response = s.post(urljoin(BASE_URL, '/posts'), data=data, allow_redirects=False)
        id = response.headers['X-ID']
        assert response.status_code == 302

        new_data = {'title': '', 'body': ''}
        response = s.post(urljoin(BASE_URL, f'/posts/{id}/update'), data=new_data, allow_redirects=False)
        assert response.status_code == 422
