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
    page = request.args.get('page', 1, type=int)
    per = request.args.get('per', 5, type=int)
    beg_ind = (page - 1) * per
    end_ind = page*per
    companies_at_page = companies[beg_ind : end_ind]
    print('request.args', request.args, 'beg_ind', beg_ind, 'end_ind', end_ind)
    return companies_at_page
# END