from urllib.parse import urljoin

import requests

BASE_URL = 'http://localhost:8000'


def test_has_form():
    response = requests.get(urljoin(BASE_URL, '/courses/new'))
    assert 'title' in response.text
    assert 'paid' in response.text


def test_validate_empty_form():
    data = {'title': '', 'paid': ''}
    response = requests.post(urljoin(BASE_URL, '/courses'), data=data)
    assert response.status_code == 422
    assert "Can&#39;t be blank" in response.text


def test_validate_empty_paid():
    data = {'title': 'How to Foobar', 'paid': ''}
    response = requests.post(urljoin(BASE_URL, '/courses'), data=data)
    assert "Can&#39;t be blank" in response.text
    assert 'How to Foobar' in response.text


def test_validate_empty_title():
    data = {'title': '', 'paid': '1'}
    response = requests.post(urljoin(BASE_URL, '/courses'), data=data)
    assert "Can&#39;t be blank" in response.text


def test_escaping():
    data = {'title': '<script></script>', 'paid': ''}
    response = requests.post(urljoin(BASE_URL, '/courses'), data=data)
    assert '&lt;script&gt;&lt;/script&gt;' in response.text


def test_post():
    data = {'title': '<script></script>', 'paid': '1'}
    response = requests.post(
        urljoin(BASE_URL, '/courses'),
        data=data,
        allow_redirects=False
    )
    assert response.status_code == 302
    response = requests.post(
        urljoin(BASE_URL, '/courses'),
        data=data)
    assert '&lt;script&gt;&lt;/script&gt;' in response.text
