import os

from flask import (
    Flask,
    flash,
    get_flashed_messages,
    make_response,
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


@app.route('/posts/new')
def new_post():
    post = {}
    errors = {}
    return render_template(
        'courses/new.html',
        post=post,
        errors=errors,
    )


@app.post('/posts')
def posts_post():
    repo = PostsRepository()
    data = request.form.to_dict()
    errors = validate(data)
    if errors:
        return render_template(
            'courses/new.html',
            post=data,
            errors=errors,
            ), 422
    id = repo.save(data)
    flash('Post has been created', 'success')
    resp = make_response(redirect(url_for('posts_get')))
    resp.headers['X-ID'] = id
    return resp


# BEGIN (write your solution here)
@app.route("/posts/<id>/update", methods = ['GET', 'POST'])
def posts_update(id):
    repo = PostsRepository()
    posts = repo.content()
    post = repo.find(id)
    if request.method == 'GET':
        return render_template(
        'courses/edit.html',
        post=post,
        errors={}
        )
    if request.method == 'POST':
        data = request.form.to_dict()
        data["id"] = id
        errors = validate(data)
        if errors:
                return render_template(
                'courses/edit.html',
                post=data,
                errors=errors), 422
        posts = repo.content()
        post["title"] = data["title"]
        post["body"] = data["body"]
        repo.save(post)
        print("yyyyyyy")
        #flash('Post has been updated', 'success')
    return redirect(url_for('posts_get'))
# END
