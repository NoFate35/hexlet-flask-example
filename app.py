from flask import Flask, flash, redirect, render_template, request, session
import os
import psycopg
import secrets
from dotenv import load_dotenv
secret = secrets.token_urlsafe(32)

from repository import Repository, generate_posts

load_dotenv()
from validator import validate


app = Flask(__name__)
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
#print('app.config:', app.config['DATABASE_URL'])
app.secret_key = secret

#conn = psycopg.connect('postgresql://u0_a441:@localhost/flaskdb')
    
repo = Repository()


@app.before_request
def initialize_data():
    if not session.get("initialized"):
        generate_posts(repo, 20)
        session["initialized"] = True


@app.route("/")
def index():
    return render_template("index.html")


# BEGIN (write your solution here)

# END
