import re
from urllib.parse import urljoin

import requests
from repository import word_list

BASE_URL = "http://localhost:8000"


def test_search_post():
    with requests.Session() as s:
        response = s.get(
            urljoin(BASE_URL, "/posts"),
            allow_redirects=True,
        )
        assert response.status_code == 200
        posts_count = response.text.count("<li>")
        assert posts_count == 20

        word = "foobar"
        response = s.get(
            urljoin(BASE_URL, f"/posts?term={word}"),
            allow_redirects=True,
        )
        assert response.status_code == 200
        assert word in response.text
        posts_count = response.text.count(word)
        assert posts_count == 4

        wrong_word = "wrongword"
        response = s.get(
            urljoin(BASE_URL, f"/posts?term={wrong_word}"),
            allow_redirects=True,
        )
        assert response.status_code == 200
        posts_count = response.text.count(wrong_word)
        assert posts_count == 1


def test_post_suggestions():
    with requests.Session() as s:
        response = s.get(
            urljoin(BASE_URL, "/posts"),
            allow_redirects=True,
        )
        post_match = re.search(
            r'(foobar. <a href="/posts/[a-f0-9-]+)"', response.text
        ).group(1)
        post_url = re.search(r"/posts/[a-f0-9-]+", post_match).group(0)
        response = s.get(
            urljoin(BASE_URL, f"{post_url}"),
            allow_redirects=True,
        )
        assert response.status_code == 200
        posts_count = response.text.count("foobar")
        assert posts_count == 4
