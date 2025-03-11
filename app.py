from flask import Flask, json, redirect, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    cart = json.loads(request.cookies.get('cart', json.dumps({})))
    return render_template('index.html', cart=cart)


# BEGIN (write your solution here)

# END
