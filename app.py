from flask import (
    Flask,
    flash,
    get_flashed_messages,
    render_template,
    redirect,
    url_for
)
import os

app = Flask(__name__)

app.secret_key = "secret_key"

#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# BEGIN (write your solution here)
@app.get('/')
def get_courses():
    messages = get_flashed_messages(with_categories = True)
    return render_template('courses/index.html', messages=messages)

@app.post('/courses/')
def redirect_courses():
    flash('Course Added ', 'success')
    return redirect(url_for('get_courses'))
# END
