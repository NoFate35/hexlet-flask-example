from flask import Flask, redirect, render_template, request
# BEGIN (write your solution here)

# END
import os

from data import Repository


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


repo = Repository()


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/courses')
def courses_get():
    courses = repo.content()
    return render_template(
        'courses/index.html',
        courses=courses,
        )


# BEGIN (write your solution here)

# END
