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
import secrets

secret = secrets.token_urlsafe(32)


app = Flask(__name__)
app.secret_key = secret
#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


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
        'index_session.html',
        messages=messages,
        current_user=current_user,
        )


# BEGIN (write your solution here)
info = app.logger.info
debug = app.logger.debug
@app.route('/session/new', methods=['POST'])
def session_new():
    info('start session_new')
    #debug('session %s', session['user'])
    user = get_user(request.form, users)
    if user is None:
        info('user is None: %s', user)
        flash('Wrong password or name')
        return redirect(url_for('index'))
    session['user'] = user
    debug('session: %s', session['user'])
    return redirect(url_for('index'))

@app.route('/session/delete', methods=['POST', 'DELETE'])
def session_delete():
    info("start session_delete")
    session.pop('user')
    return redirect(url_for('index'))
# END