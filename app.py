from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
import os

from repository import get_db, ProductsRepository
from validator import validate


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

repo = ProductsRepository(get_db(app))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/products')
def products():
    products = repo.get_entities()
    return render_template('products/index.html', products=products)


# BEGIN (write your solution here)

# END