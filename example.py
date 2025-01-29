from flask import Flask
from flask import request
#from flask import make_response
from flask import render_template

app = Flask(__name__)

users = [
    {'id': 1, 'name': 'mike'},
    {'id': 2, 'name': 'mishel'},
    {'id': 3, 'name': 'adel'},
    {'id': 4, 'name': 'keks'},
    {'id': 5, 'name': 'kamila'},
    {"id": 8803332605, "name": 'Cj'}
]

@app.route('/users')
def get_users():
    query = request.args.get('query')
    print("запрос от Егора", query)
    if query is None:
        return render_template('users/index.html',
                           users = users)
    filtered_users = filter(lambda user: query in user['name'], users)
    
    return render_template('users/index.html',
                           users = filtered_users,
                           search = query)
    