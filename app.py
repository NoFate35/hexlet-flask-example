from flask import Flask, jsonify

from data import generate_companies

companies = generate_companies(100)

app = Flask(__name__)


@app.route('/')
def index():
    return 'open something like (you can change id): /companies/5'


# BEGIN (write your solution here)

# END
