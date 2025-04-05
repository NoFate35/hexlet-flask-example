import os
import secrets
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, session
from repository import Comment, CommentStatus, Repository, generate_posts
from validator import check_spam, check_triggers

secret = secrets.token_urlsafe(32)

load_dotenv()


app = Flask(__name__)
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
#print('app.config:', app.config['DATABASE_URL'])
app.secret_key = secret

#conn = psycopg.connect('postgresql://u0_a441:@localhost/flaskdb')
    
repo = Repository()


@app.before_request
def initialize_data():
    if not session.get("initialized"):
        generate_posts(repo, 4)
        session["initialized"] = True


@app.route("/")
def index():
    return render_template("index.html")


# BEGIN (write your solution here)
debug = app.logger.debug

@app.route('/posts')
def posts_route():
    query = request.args.get('term')
    posts = repo.get_all_posts()
    filter_posts = []
    if query:
        for post in posts:
            if (query in post.title) or (query in post.content):
                debug("query: %s, post.title: %s \n post.body: %s", query, post.title, post.content)
                filter_posts.append(post)
                posts = filter_posts
    return render_template('courses/index.html', posts=posts, query=query)


@app.route('/posts/<uuid:post_id>')
def posts_show(post_id):
    debug("ggggggggggggggggggggg")
    post = repo.get_post(post_id)
    similar_posts = []
    for word in post.title.split():
        similar_posts_for_word = repo.search_posts(word)
        for similar_post in similar_posts_for_word:
            if (similar_post not in similar_posts) and (similar_post != post):
                similar_posts.append(similar_post)
                debug("simmmmm: %s \n", similar_post)
    return render_template('courses/view.html', post=post, similar_posts=similar_posts)
# END