import os

import secrets
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from repository import Comment, CommentStatus, Repository, generate_posts
from validator import check_spam, check_triggers

secret = secrets.token_urlsafe(32)
#print('тоооокен', secret)

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


@app.route("/posts")
def list_posts():
    all_posts = repo.get_all_posts()
    return render_template("courses/index.html", posts=all_posts)


@app.route("/posts/<uuid:post_id>")
def view_post(post_id):
    post = repo.get_post(post_id)
    if not post:
        abort(404)

    post_comments = repo.get_comments_by_post(post_id)
    return render_template("courses/view.html", post=post, comments=post_comments)


# BEGIN (write your solution here)
debug = app.logger.debug
@app.route('/posts/<uuid:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    text_comment = request.form.to_dict()
    spam = check_spam(text_comment["text"])
    if not spam:
        trigger = check_triggers(text_comment["text"])
        comment_status = CommentStatus.APPROVED
        comment = Comment(
        post_id = post_id,
        text = text_comment["text"],
        status = CommentStatus.WAITING if trigger else CommentStatus.APPROVED
        )
        if trigger:
            flash("Ваш комментарий отправлен на проверку", "info")
        else:
            flash("Комментарий успешно добавлен", "success")

        repo.save_comment(comment)
        return redirect(url_for('view_post', post_id=post_id))
    flash("Комментарий содержит спам", "error")
    return redirect(f"/posts/{post_id}")


@app.route("/moderate/<uuid:comment_id>", methods=['POST'])
def moderate_comment(comment_id):
    comment = repo.get_comment(comment_id)
    if not comment:
        abort(404)
    action = request.form.to_dict()
    if action['action'] == 'approve':
        comment.status = CommentStatus.APPROVED
        flash("Комментарий одобрен", "success")
    else:
        comment.status = CommentStatus.REJECTED
        flash("Комментарий отклонен", "warning")
    repo.save_comment(comment)
    debug("comment: %s", comment)
    return redirect(url_for('moderate_comments'))
# END


@app.route("/moderate")
def moderate_comments():
    waiting_comments = repo.get_waiting_comments()
    #debug("waiting comments: %s", waiting_comments)

    comments_with_context = []
    for comment in waiting_comments:
        post = repo.get_post(comment.post_id)
        if post:
            context = {"post_title": post.title, "comment": comment}
            comments_with_context.append(context)

    return render_template("courses/moderate.html", comments=waiting_comments)
