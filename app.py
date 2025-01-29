from flask import Flask, render_template

from data import generate_users

users = generate_users(100)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# BEGIN (write your solution here)
@app.route('/users')
def get_users():
    return render_template('users/show.html', users=users)

@app.route('/users/<int:id>')
def get_user(id):
    filtered_users = filter(lambda user: user['id'] == id, users)
    user = next(filtered_users, None)
    if user == None:
        return 'Page not found', 404
    return render_template('users/index.html', user=user )

@app.route('/courses/')
def get_courses():
    return render_template('courses/layout.html')

@app.route('/courses/<int:id>')
def get_course(id):
    return render_template('courses/index.html', id = id)
# END
