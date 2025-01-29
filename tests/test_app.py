from urllib.parse import urljoin

import requests

BASE_URL = 'http://localhost:8000'


def test_has_form():
    response = requests.get(urljoin(BASE_URL, '/users'))
    assert 'form' in response.text


def test_users():
    response = requests.get(urljoin(BASE_URL, '/users'))
    assert 'Warren' in response.text
    assert 'Amanda' in response.text


def test_starts_with_term():
    response = requests.get(urljoin(BASE_URL, '/users?term=al'))
    assert 'Alyssa' in response.text
    assert 'Alexa' in response.text
    assert 'Allison' in response.text
    assert 'Sarah' not in response.text


def test_with_term_in_middle():
    response = requests.get(urljoin(BASE_URL, '/users?term=al'))
    assert 'Gerald' not in response.text
    assert 'Randall' not in response.text


def test_not_found_term():
    response = requests.get(urljoin(BASE_URL, '/users?term=aaaaa'))
    assert 'aaaaa' in response.text