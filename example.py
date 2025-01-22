from flask import Flask
from flask import jsonify

from faker import Faker

fake = Faker()
fake.seed_instance(1234)

domains = [fake.domain_name() for i in range(10)]
phones = [fake.phone_number() for i in range(10)]

# Это callable WSGI-приложение
app = Flask(__name__)


@app.route("/")
def index():
    return "go to the /phones or /domains" 

@app.route('/phones')
def get_phones():
    return jsonify(phones)

@app.route("/domains")
def get_domains():
    return jsonify(domains)