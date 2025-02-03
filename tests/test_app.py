from urllib.parse import urljoin

import requests

BASE_URL = 'http://localhost:8000'


def test_fisrt_page():
    response = requests.get(urljoin(BASE_URL, '/posts'))
    assert 'Theory key since close film available' in response.text
    assert 'Approach onto clearly newspaper' in response.text


def test_second_page():
    response = requests.get(urljoin(BASE_URL, '/posts?page=2'))
    prev_page = '?page=1'
    next_page = '?page=3'
    assert prev_page in response.text
    assert next_page in response.text

    assert 'Theory key since close film available' not in response.text
    assert 'Economic at stay staff store no' in response.text


def test_get_post():
    response = requests.get(urljoin(BASE_URL, '/posts/always-discuss-move'))
    assert 'Approach onto clearly newspaper' in response.text
    assert 'Visit side whatever.' in response.text


def test_post_not_found():
    response = requests.get(urljoin(BASE_URL, '/posts/not-found-post'))
    assert response.status_code == 404
    assert 'Page not found' in response.text
