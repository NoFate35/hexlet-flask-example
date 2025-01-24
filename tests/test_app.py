import json
from urllib.parse import urljoin

import requests

BASE_URL = 'http://localhost:8080'


def test_companies1():
    expected = {'id': 1, 'name': 'Cooper-Perez', 'phone': '848-357-4398'}
    response = requests.get(urljoin(BASE_URL, '/companies/1'))
    assert json.loads(response.text) == expected


def test_companies2():
    expected = {'id': 98, 'name': 'Lara-Robinson', 'phone': '554-371-9416'}
    response = requests.get(urljoin(BASE_URL, '/companies/98'))
    assert json.loads(response.text) == expected


def test_companies_not_found():
    response = requests.get(urljoin(BASE_URL, '/companies/12341234'))
    assert response.text == 'Page not found'
    assert response.status_code == 404
