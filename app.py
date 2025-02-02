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
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# BEGIN (write your solution here)

# END
