from urllib.parse import urljoin

import requests

BASE_URL = 'http://localhost:8000'


def test_form():
    response = requests.get(urljoin(BASE_URL, '/posts/new'))
    assert 'title' in response.text
    assert 'body' in response.text


def test_wrong_post_data():
    data = {'title': '', 'body': ''}
    response = requests.post(urljoin(BASE_URL, '/posts'), data=data)
    assert response.status_code == 422
    assert "Can&#39;t be blank" in response.text

    data = {'title': 'Foobar', 'body': ''}
    response = requests.post(urljoin(BASE_URL, '/posts'), data=data)
    assert response.status_code == 422
    assert "Can&#39;t be blank" in response.text
    assert 'Foobar' in response.text

    data = {'title': '', 'body': 'Barbaz'}
    response = requests.post(urljoin(BASE_URL, '/posts'), data=data)
    assert response.status_code == 422
    assert "Can&#39;t be blank" in response.text
    assert 'Barbaz' in response.text


def test_create_posts():
    with requests.Session() as s:
        data = {'title': 'first', 'body': 'first_body'}
        response = s.post(urljoin(BASE_URL, '/posts'), data=data, allow_redirects=False)  # noqa: E501

        assert response.status_code == 302

        response = s.get(urljoin(BASE_URL, '/posts'))
        assert 'Post has been created' in response.text
        assert 'first' in response.text

        data = {'title': 'second', 'body': 'second_body'}
        response = s.post(urljoin(BASE_URL, '/posts'), data=data)

        assert 'Post has been created' in response.text
        assert 'first' in response.text
        assert 'second' in response.text
