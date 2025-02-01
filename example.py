from flask import Flask, render_template, request, redirect


import json
import uuid



app = Flask(__name__)

users = json.load(open('data.json', 'r'))


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/users/')
def search_users():
    with open('data.json', 'r') as f:
        users = json.load(f)

    query = request.args.get('query', '')

    if query:
        filter_users = [user for user in users if query.lower() in user['nickname'].lower()]
        print('filter_users', filter_users )
        users = filter_users
    
    return render_template('users/index.html',
                            users=users,
                            query=query)


@app.post('/users')
def users_post():
    user_data = request.form.to_dict()
    print('user', user_data)
    errors = validate(user_data)
    print('errors', errors)
    if errors:
        return render_template('users/new.html',
                               user=user_data,
                               errors=errors
                               )
    id = str(uuid.uuid4())
    print('uuid', id)
    user = {
        'id': id,
        'nickname':user_data['nickname'],
        'email': user_data['email']
    }
    users.append(user)
    with open("data.json", "w") as f:
        json.dump(users, f)
    return redirect('/users', code=302)
    
@app.get('/users/new')
def users_get():
    user = {'nickname': '',
            'email': '',
            }
    errors = {}
    return render_template('users/new.html',
    user=user, errors=errors)


def validate(user):
    errors = {}
    if not user['nickname']:
        errors['name'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"
    return errors

