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
    #print('posssts', posts)
    return render_template('courses/index.html',
                           posts=posts)

@app.get('/posts/<slug>')
def posts_show(slug):
    post = repo.find(slug)
    if not post:
        return 'Page not found', 404
    return render_template('courses/show.html', post=post)
# END

