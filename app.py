from flask import Flask, json, redirect, render_template, request, make_response, url_for

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    app.logger.info('start main index')
    app.logger.debug('cookies: %s', request.cookies)
    cart = json.loads(request.cookies.get('cart', json.dumps({})))
    return render_template('index_carts.html', cart=cart)


# BEGIN (write your solution here)
@app.route('/cart-items', methods=['POST'])
def carts_cookies_add():
    app.logger.info('start carts_cookies_add')
    #app.logger.debug('request.form.to_dict: %s', request.form.to_dict())
    id = request.form['item_id']
    name = request.form['item_name']
    cart = json.loads(request.cookies.get('cart', json.dumps({})))
    result = cart.get(item['item_id'])
    app.logger.debug('cart: %s, item: %s', cart, item)
    if result is None:
        cart[item['item_id']] = {'name': item['item_name'], 'count': 0}
        app.logger.debug('cart is None, cart: %s', cart)
    cart[item['item_id']]['count'] += 1
    app.logger.debug("cart after add cart[item['item_id']]['count']: %s", cart[item['item_id']]['count'])
    encoded_сart = json.dumps(cart)
    response = redirect('/')
    response.set_cookie('cart', encoded_сart)
    #app.logger.debug('request.form.to_dict: %s', request.form.to_dict())
    return response

@app.route('/cart-items/clean', methods=['POST'])
def carts_cookies_clean():
    encoded_сart = json.dumps({})
    response = redirect('/')
    response.delete_cookie('cart')
    return response
    
# END
