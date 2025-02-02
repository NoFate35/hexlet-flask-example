from urllib.parse import urljoin

import requests

BASE_URL = 'http://localhost:8080'


def test_flash():
    response = requests.get(urljoin(BASE_URL, '/'))
    assert 'Course Added' not in response.text

    response = requests.post(urljoin(BASE_URL, '/courses'), data=[])
    assert 'Course Added' in response.text

    response = requests.get(urljoin(BASE_URL, '/'))
    assert 'Course Added' not in response.text

