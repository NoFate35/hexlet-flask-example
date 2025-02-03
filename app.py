from flask import Flask, render_template, request
from repository import PostsRepository

app = Flask(__name__)

repo = PostsRepository(50)


@app.route('/')
def index():
    return render_template('index.html')


# BEGIN (write your solution here)

# END

