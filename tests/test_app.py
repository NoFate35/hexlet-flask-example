import re
from urllib.parse import urljoin

import requests
from repository import ids

BASE_URL = "http://localhost:8000"


def test_add_comment():
    with requests.Session() as s:
        post_id = ids[0]
        text = "TEST COMMENT TEXT"
        response = s.post(
            urljoin(BASE_URL, f"/posts/{post_id}/comments"),
            data={"text": text},
            allow_redirects=True,
        )

        response = s.get(urljoin(BASE_URL, f"/posts/{post_id}"))
        assert response.status_code == 200
        assert text in response.text


def test_add_spam_comment():
    with requests.Session() as s:
        post_id = ids[0]
        text = "TEST SPAM COMMENT"
        response = s.post(
            urljoin(BASE_URL, f"/posts/{post_id}/comments"),
            data={"text": text},
            allow_redirects=False,
        )
        assert response.status_code == 302

        response = s.get(urljoin(BASE_URL, f"/posts/{post_id}"))
        assert response.status_code == 200
        assert text not in response.text


def test_approve_moderation_comment():
    with requests.Session() as s:
        post_id = ids[0]
        text = "TEST http GOODTEXT"
        response = s.post(
            urljoin(BASE_URL, f"/posts/{post_id}/comments"),
            data={"text": text},
            allow_redirects=True,
        )

        response = s.get(urljoin(BASE_URL, f"/posts/{post_id}"))
        assert response.status_code == 200
        assert text not in response.text, "Comment on moderation"

        response = s.get(urljoin(BASE_URL, "/moderate"))
        assert text in response.text, "Comment in moderation list"

        comment_id = re.search(r'/moderate/([a-f0-9-]+)"', response.text).group(1)

        # Approve the comment
        response = s.post(
            urljoin(BASE_URL, f"/moderate/{comment_id}"),
            data={"action": "approve"},
            allow_redirects=True,
        )
        response = s.get(urljoin(BASE_URL, f"/posts/{post_id}"))
        assert text in response.text, "Comment should be visible after approval"


def test_reject_moderation_comment():
    with requests.Session() as s:
        post_id = ids[0]
        text = "TEST http BADTEXT"
        response = s.post(
            urljoin(BASE_URL, f"/posts/{post_id}/comments"),
            data={"text": text},
            allow_redirects=True,
        )

        response = s.get(urljoin(BASE_URL, f"/posts/{post_id}"))
        assert response.status_code == 200
        assert text not in response.text, "Comment on moderation"

        response = s.get(urljoin(BASE_URL, "/moderate"))
        assert text in response.text, "Comment in moderation list"

        comment_id = re.search(r'/moderate/([a-f0-9-]+)"', response.text).group(1)

        # Reject the comment
        response = s.post(
            urljoin(BASE_URL, f"/moderate/{comment_id}"),
            data={"action": "reject"},
            allow_redirects=True,
        )
        response = s.get(urljoin(BASE_URL, f"/posts/{post_id}"))
        assert text not in response.text, "Comment should not be visible after approval"
