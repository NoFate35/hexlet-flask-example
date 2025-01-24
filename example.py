from flask import Flask
from flask import request
from flask import make_response


# Это callable WSGI-приложение
app = Flask(__name__)

@app.route('/hello')
def hello():
    # создаем объект response
    response = make_response('Hello, World!')
    # Устанавливаем заголовок
    response.headers['X-MyHeader'] = 'Thats my header!'
    # Меняем тип ответа
    response.mimetype = 'text/plain'
    # Задаем статус
    response.status_code = 201
    # Устанавливаем cookie
    response.set_cookie('super-cookie', '42')
    return response

@app.post('/users')
def get_users():
     response = make_response('hhhhhhhhh')
     response.headers['X-MyHeader'] = 'yooooo'
     return response
