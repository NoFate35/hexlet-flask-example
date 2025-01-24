from flask import Flask, jsonify, request

from data import generate_companies

companies = generate_companies(100)

app = Flask(__name__)


@app.route('/')
def index():
    return "<a href='/companies'>Companies</a>"


# BEGIN (write your solution here)
@app.route('/companies')
def get_companies():
    print('requuuuuest args', request.args)
    return {'u': 6}
# END