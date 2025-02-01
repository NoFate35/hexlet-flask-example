from flask import Flask, redirect, render_template, request
import secrets
# BEGIN (write your solution here)
from validator import validate
# END
import os

from data import Repository


app = Flask(__name__)

secret = secrets.token_urlsafe(32)
app.secret_key = secret
#app.config['SECRET_KEY'] = os.getenv('iiiiififjf')


repo = Repository()


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/courses/')
def courses_get():
    courses = repo.content()
    return render_template(
        'courses/index.html',
        courses=courses,
        )


# BEGIN (write your solution here)
@app.post('/courses')
def courses():
    course = request.form.to_dict()
    errors = validate(course)
    if errors:
        return render_template('/courses/new.html',
                               course=course,
                               errors=errors), 422
    repo.save(course)
    return redirect('/courses', code=302)

@app.get('/courses/new')
def make_new():
    course = {'title': '',
              'paid': ''}
    errors = {}
    return render_template('/courses/new.html',
                           course=course,
                           errors=errors)
# END
