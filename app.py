from flask import Flask, flash, redirect, render_template, request, session
import os
import psycopg
import secrets

secret = secrets.token_urlsafe(32)

from repository import get_db, ProductsRepository
from validator import validate


app = Flask(__name__)
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
#print('app.config:', app.config['DATABASE_URL'])
app.secret_key = secret

#conn = psycopg.connect('postgresql://u0_a441:@localhost/flaskdb')
    
#repo = ProductsRepository(get_db(app))


PROMOCODES = {"SALE10": 10, "SALE20": 20, "SALE30": 30}
PRODUCTS = {
    "1": {"name": "apple", "price": 50},
    "2": {"name": "orange", "price": 45},
    "3": {"name": "banana", "price": 30},
}


@app.route("/")
def product_list():
    return render_template("courses/products.html", products=PRODUCTS)


@app.route("/cart/add/<product_id>", methods=["POST"])
def add_to_cart(product_id):
    cart = session.get("cart", {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session["cart"] = cart
    flash("Товар добавлен в корзину", "info")
    return redirect("/")


# BEGIN (write your solution here)
debug = app.logger.debug

@app.route('/cart')
def cart_list():
    total_price = 0
    cart = session.get("cart", {})
    filtered_products = []
    for key, value in cart.items():
        filtered_products.append({'name': PRODUCTS[key]['name'], 'quantity': value})
        total_price += PRODUCTS[key]['price'] * value
        #debug('currta %s, %s', filtered_products, total_price)
    return render_template('courses/cart.html', products=filtered_products, total_price=total_price)
    
    
    return render_template('courses/cart.html')
"""
def filter_products(cart):
    filtered_products = {}
    for x in cart.keys():
        if x in PRODUCTS.keys():
            debug('cart fff %s', PRODUCTS[x])
        #if x in PRODUCTS.keys():
            #filter_pr
   """     
# END
