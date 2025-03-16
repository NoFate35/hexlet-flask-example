from flask import Flask, render_template, request, redirect, flash, get_flashed_messages, url_for, session
from .flask_repository import UserRepository
import psycopg2
import json
import uuid
import secrets

secret = secrets.token_urlsafe(32)
app = Flask(__name__)
app.secret_key = secret
app.logger.setLevel('DEBUG')
app.secret_key = secret

try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect(dbname='flaskdb', user='ivan', password='', host='')
except:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Can`t establish connection to database')
"""
try:
    # пытаемся подключиться к базе данных
    #conn = psycopg2.connect('postgresql://u0_a441@localhost/flaskdb')
    conn = psycopg2.connect("postgresql://ivan@localhost/flaskdb")
except:
    # в случае сбоя подключения будет выведено сообщение  в STDOUT
    print('Can`t establish connection to database')
"""
repo = UserRepository(conn)

@app.route('/')
def index():
    app.logger.info('render main template')
    return render_template('index.html')


@app.get('/users/')
def users_index():
    app.logger.info('start users_index')
    query = request.args.get('query', '')
    if query:
        app.logger.info('query = True')
        users = repo.get_by_term(query)
    else:
        users = repo.get_content()
    messages = get_flashed_messages(with_categories=True)
    app.logger.info('render_template users/index.html')
    return render_template('users/index.html',
                            users=users,
                            query=query,
                            messages=messages)

@app.route('/users/<int:id>')
def users_show(id):
    app.logger.info('start users_show - users/<id>')
    user = repo.find(id)
    if not user:
        app.logger.debug('user not found')
        return 'Page not found', 404
    app.logger.debug('render template users/show.html')
    return render_template('users/show.html',
    user=user)

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
    #id = str(uuid.uuid4())
    user = {
        #'id': id,
        'nickname':user_data['nickname'],
        'email': user_data['email']
    }
    repo.save(user)
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

@app.route('/users/<int:id>/edit')
def users_edit(id):
    app.logger.info('start edit user render template')
    app.logger.debug(users_edit, id)
    user = repo.find(id)
    app.logger.debug('render template users/edit.html')
    return render_template("users/edit.html", user=user, errors={})

@app.route("/users/<int:id>/patch", methods=["POST"])
def users_patch(id):
    app.logger.info('start patching user')
    data = request.form.to_dict()
    user = repo.find(id)
    errors = validate(data)
    if errors:
        app.logger.debug('errors have been found')
        data['id'] = user['id']
        return render_template("users/edit.html", user=data, errors=errors), 422
    app.logger.debug('no errors')
    user["nickname"] = data["nickname"]
    user["email"] = data["email"]
    repo.save(user)
    flash("User has been updated", 'success')
    app.logger.debug('redirect for render all users')
    return redirect(url_for('users_index'))
    
@app.post('/users/<int:id>/delete')
def users_delete(id):
    app.logger.info('start users delit')
    user = repo.find(id)
    repo.delete(user['id'])
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

