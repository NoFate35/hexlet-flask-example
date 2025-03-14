from flask import Flask, render_template, request, redirect, flash, get_flashed_messages, url_for, session

import psycopg2
import json
import uuid
import secrets

secret = secrets.token_urlsafe(32)
app = Flask(__name__)
app.secret_key = secret
app.logger.setLevel('DEBUG')
app.secret_key = secret
"""
try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect(dbname='', user='u0_a441',  host='lockalhost')
except:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Can`t establish connection to database')
"""
try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect('postgresql://u0_a441@localhost/flaskdb')
except:
    # в случае сбоя подключения будет выведено сообщение  в STDOUT
    print('Can`t establish connection to database')

@app.route('/')
def index():
    app.logger.info('render main template')
    return render_template('index.html')


@app.get('/users/')
def users_index():
    app.logger.info('start users_index')
    users = session.get('users')
    if users is None:
        session['users'] = []
        users = {'nickname': '', 'email': ''}
    query = request.args.get('query', '')
    if query:
        app.logger.info('query = True')
        filter_users = [user for user in users if query.lower() in user['nickname'].lower()]
        users = filter_users
    messages = get_flashed_messages(with_categories=True)
    app.logger.info('render_template users/index.html')
    return render_template('users/index.html',
                            users=users,
                            query=query,
                            messages=messages)

@app.route('/users/<id>')
def users_show(id):
    app.logger.info('start users_show - users/<id>')
    users = session.get('users')
    if users is None:
        session['users'] = []
        users = {'nickname': '', 'email': ''}
    user = list(user for user in users if user['id'] == id)
    if not user:
        app.logger.debug('user not found')
        return 'Page not found', 404
    app.logger.debug('render template users/show.html')
    return render_template('users/show.html',
    user=user[0])

@app.post('/users/')
def users_post():
    app.logger.info('start adding user users_post')
    user_data = request.form.to_dict()
    errors = validate(user_data)
    if errors:
        app.logger.debug('errors have been found, errors: %s', errors)
        return render_template('users/new.html',
                               user=user_data,
                               errors=errors
                               )
    id = str(uuid.uuid4())
    user = {
        'id': id,
        'nickname':user_data['nickname'],
        'email': user_data['email']
    }
    res = session.get('users')
    if res is None:
        session['users'] = []
    session['users'].append(user)
    flash('User was added successfully', 'success')
    app.logger.debug('user was added - success')
    return redirect(url_for('users_index'), code=302)
    
@app.get('/users/new')
def users_new():
    app.logger.info('start render adding user form')
    user = {'nickname': '',
            'email': '',
            }
    errors = {}
    app.logger.debug('render template users/new')
    return render_template('users/new.html',
    user=user, errors=errors)

@app.route('/users/<id>/edit')
def users_edit(id):
    app.logger.info('start edit user render template')
    app.logger.debug(users_edit, id)
    users = session.get('users')
    if users is None:
        session['users'] = []
        users = {'nickname': '', 'email': ''}
    user = [user for user in users if user["id"] == id][0]
    errors = {}
    app.logger.debug('render template users/edit.html')
    return render_template("users/edit.html", user=user, errors=errors)

@app.route("/users/<id>/patch", methods=["POST"])
def users_patch(id):
    app.logger.info('start patching user')
    data = request.form.to_dict()
    users = session.get('users')
    if users is None:
        session['users'] = []
        users = {'nickname': '', 'email': ''}
    user = [user for user in users if user["id"] == id][0]
    errors = validate(data)
    if errors:
        app.logger.debug('errors have been found')
        data['id'] = user['id']
        return render_template("users/edit.html", user=data, errors=errors), 422
    app.logger.debug('no errors')
    users.remove(user)
    user["nickname"] = data["nickname"]
    user["email"] = data["email"]
    users.append(user)
    with open("data.json", "w") as f:
        json.dump(users, f)
    flash("User has been updated", 'success')
    app.logger.debug('redirect for render all users')
    return redirect(url_for('users_index'))
    
@app.post('/users/<id>/delete')
def users_delete(id):
    app.logger.info('start users delit')
    users = session.get('users')
    if users is None:
        session['users'] = []
        users = {'nickname': '', 'email': ''}
    user = list(user for user in users if user['id'] == id)[0]
    users.remove(user)
    app.logger.debug('user: %s', user)
    flash('Пользователь удален', 'success')
    return redirect(url_for('users_index'), code=302)
    
def validate(user):
    app.logger.info('start validate data')
    errors = {}
    if not user['nickname']:
        errors['nickname'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"
    return errors

