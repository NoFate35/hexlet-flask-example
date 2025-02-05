from flask import Flask, render_template, request
from repository import PostsRepository

app = Flask(__name__)

repo = PostsRepository(50)


@app.route('/')
def index():
    return render_template('index.html')


# BEGIN (write your solution here)
@app.route('/posts')
def posts_index():
    posts = repo.content()
    page = request.args.get('page', 1, type=int)
    per = request.args.get('per', 5, type=int)
    prev_page = (page - 1) * per
    current_page = page*per
    posts_at_page = posts[prev_page:current_page]
    print('page', page)
    return render_template('courses/index.html', posts=posts_at_page, page=page)

@app.get('/posts/<slug>')
def posts_show(slug):
    post = repo.find(slug)
    if not post:
        return 'Page not found', 404
    return render_template('courses/show.html', post=post)
# END

