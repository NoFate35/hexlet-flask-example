import os

from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from repository import PostsRepository
from validator import validate
import secrets


app = Flask(__name__)
#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
secret = secrets.token_urlsafe(32)
app.secret_key = secret

@app.route('/')
def index():
    return render_template('index.html')


@app.get('/posts')
def posts_get():
    repo = PostsRepository()
    messages = get_flashed_messages(with_categories=True)
    posts = repo.content()
    return render_template(
        'courses/index.html',
        posts=posts,
        messages=messages,
        )


# BEGIN (write your solution here)
@app.get('/posts/new')
def posts_new():
    post = {'title': '', 'body': ''}
    errors = {}
    return render_template('courses/new.html')


@app.post('/posts')
def posts_index():
    repo = PostsRepository()
    post = request.form.to_dict()
    #print("post to dict", post)
    errors = validate(post)
    if errors:
        return render_template('courses/new.html', errors=errors, post=post), 422
    repo.save(post)
    flash('Post has been created', 'success')
    return redirect(url_for('posts_get'))
# END
