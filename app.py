from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from hashlib import sha256
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


users = [
    {'name': 'tota', 'password': sha256(b'password123').hexdigest()},
    {'name': 'alice', 'password': sha256(b'donthackme').hexdigest()},
    {'name': 'bob', 'password': sha256(b'qwerty').hexdigest()},
]


def get_user(form_data, repo):
    name = form_data['name']
    password = sha256(form_data['password'].encode()).hexdigest()
    for user in repo:
        if user['name'] == name and user['password'] == password:
            return user


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    current_user = session.get('user')
    return render_template(
        'index.html',
        messages=messages,
        current_user=current_user,
        )


# BEGIN (write your solution here)

# END
