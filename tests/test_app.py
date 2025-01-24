from urllib.parse import urljoin

import requests

BASE_URL = 'http://localhost:8000'


def test_companies():
    expected = [
        {'name': 'Wilson-Davis', 'phone': '001-701-915-3000'},
        {'name': 'Ford, Davis and Reeves', 'phone': '3872318719'},
        {'name': 'Holloway-Brown', 'phone': '475-943-3780x8105'},
        {'name': 'Bennett, Brown and Matthews', 'phone': '(418)632-0518'},
        {'name': 'Williams-Hill', 'phone': '8247242709'}
    ]

    response = requests.get(urljoin(BASE_URL, '/companies'))
    assert response.json() == expected


def test_companies_slice1():
    expected = [
        {'name': 'Holloway-Brown', 'phone': '475-943-3780x8105'}
    ]
    response = requests.get(urljoin(BASE_URL, '/companies?page=3&per=1'))
    assert response.json() == expected


def test_companies_slice2():
    expected = [
        {'name': 'Figueroa, Boyd and Smith', 'phone': '759-632-0497x0626'},
        {'name': 'Friedman Inc', 'phone': '001-469-858-9067'}
    ]
    response = requests.get(urljoin(BASE_URL, '/companies?page=20&per=2'))
    assert response.json() == expected
