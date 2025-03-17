from urllib.parse import urljoin

import requests

BASE_URL = 'http://localhost:8000'


def test_get_products():
    with requests.Session() as s:
        response = s.get(urljoin(BASE_URL, '/products'))
        assert response.status_code == 200

        assert 'computer' in response.text
        assert '15000'

        response = s.get(urljoin(BASE_URL, '/products/1'))
        assert 'computer' in response.text
        assert '15000' in response.text


def test_create_product():
    with requests.Session() as s:
        data = {'title': 'car', 'price': '77777'}
        response = s.post(urljoin(BASE_URL, '/products'), data=data, allow_redirects=False)
        assert response.status_code == 302

        response = s.get(urljoin(BASE_URL, '/products'))
        assert 'car' in response.text
        assert '77777' in response.text


def test_create_with_errors():
    with requests.Session() as s:
        data = {'title': '', 'price': '88888'}
        response = s.post(urljoin(BASE_URL, '/products'), data=data)
        assert response.status_code == 422
        assert "Can&#39;t be blank" in response.text

        data = {'title': 'foobar', 'price': '-77777'}
        response = s.post(urljoin(BASE_URL, '/products'), data=data, allow_redirects=False)
        assert response.status_code == 422
        assert "Can&#39;t be negative" in response.text

        response = s.get(urljoin(BASE_URL, '/products'))
        assert '88888' not in response.text
        assert 'foobar' not in response.text
