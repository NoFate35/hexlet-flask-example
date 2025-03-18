from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
import os
import psycopg
import secrets

secret = secrets.token_urlsafe(32)

from repository import get_db, ProductsRepository
from validator import validate


app = Flask(__name__)
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
print('app.config:', app.config['DATABASE_URL'])
app.secret_key = secret

#conn = psycopg.connect('postgresql://u0_a441:@localhost/flaskdb')
    
repo = ProductsRepository(get_db(app))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/products')
def products():
    products = repo.get_entities()
    messages = get_flashed_messages(with_categories=True)
    return render_template('courses/index.html', products=products, messages=messages)


# BEGIN (write your solution here)
@app.route('/products/<id>')
def products_find(id):
    product = repo.find(int(id))
    print("produuuct", isinstance(product, dict))
    return render_template('courses/index.html', products=[product], messages={})
    
@app.route('/products/new')
def new_product():
    return render_template('courses/new.html', errors={}, product={})
    
@app.route('/products', methods=['POST'])
def products_add():
    product = request.form.to_dict()
    errors = validate(product)
    if errors:
        return render_template('courses/new.html', errors=errors, product=product), 422
    repo.save(product)
    flash('Sucssess, product was added')
    print('ppproduct', product)
    return redirect(url_for('products'))
# END