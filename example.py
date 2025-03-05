from flask import Flask, render_template, request, redirect, flash, get_flashed_messages, url_for


import json
import uuid



app = Flask(__name__)

users = json.load(open('data.json', 'r'))

app.secret_key = "secret_key"

@app.route('/')
def index():
    return render_template('index.html')


@app.get('/users/')
def users_index():
    with open('data.json', 'r') as f:
        users = json.load(f)

    query = request.args.get('query', '')

    if query:
        filter_users = [user for user in users if query.lower() in user['nickname'].lower()]
        users = filter_users
    messages = get_flashed_messages(with_categories=True)
    return render_template('users/index.html',
                            users=users,
                            query=query,
                            messages=messages)

@app.route('/users/<id>')
def users_show(id):
    with open('data.json', 'r') as f:
        users = json.load(f)
    user = list(user for user in users if user['id'] == id)
    print('ttttt', user)
    if not user:
        return 'Page not found', 404
    return render_template('users/show.html',
    user=user[0])

@app.post('/users/')
def users_post():
    user_data = request.form.to_dict()
    errors = validate(user_data)
    if errors:
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
    users.append(user)
    with open("data.json", "w") as f:
        json.dump(users, f)
    flash('User was added successfully', 'success')
    return redirect(url_for('users_index'), code=302)
    
@app.get('/users/new')
def users_new():
    user = {'nickname': '',
            'email': '',
            }
    errors = {}
    return render_template('users/new.html',
    user=user, errors=errors)

@app.route('/users/<id>/edit')
def users_edit(id):
    print(users_edit, id)
    with open("data.json", "r") as f:
        users = json.load(f)
    user = [user for user in users if user["id"] == id][0]
    errors = {}
    return render_template("users/edit.html", user=user, errors=errors)

@app.route("/users/<id>/patch", methods=["POST"])
def users_patch(id):
    data = request.form.to_dict()
    with open("data.json", "r") as f:
        users = json.load(f)
    user = [user for user in users if user["id"] == id][0]
    errors = validate(data)
    if errors:
        data['id'] = user['id']
        return render_template("users/edit.html", user=data, errors=errors), 422
    users.remove(user)
    user["nickname"] = data["nickname"]
    user["email"] = data["email"]
    users.append(user)
    with open("data.json", "w") as f:
        json.dump(users, f)
    flash("User has been updated", 'success')
    return redirect(url_for('users_index'))

def validate(user):
    errors = {}
    if not user['nickname']:
        errors['nickname'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"
    return errors

