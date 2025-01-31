from flask import Flask, render_template, request, redirect

from data import generate_users

users = generate_users(100)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/users')
def users_post():
    user = request.form.to_dict()
    #errors = validate(user)
    errors = {1}
    if errors:
        return render_template(
          'users/new.html',
          user=user,
          errors=errors
        )
    #with open("data.json", "w") as f:
        #json.dump(user, f)
    #return redirect('/users', code=302)
    
@app.get('/users')
def users_get():
    user = {'name': '',
            'email': '',
            'password': '',
            'passwordConfirmation': '',
            'city': ''}
    errors = {}
    return render_template('users/new.html',
    user=user, errors=errors)

