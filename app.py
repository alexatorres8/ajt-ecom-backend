from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

# User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ('email', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Endpoint to create a new user
@app.route('/user', methods=["POST"])
def add_user():
    email = request.json['email']
    password = request.json['password']

    new_user = User(email, password)

    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)

    return product_schema.jsonify(user)

# Endpoint to query all user
@app.route("/users", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)



# Product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, item, price):
        self.item = item
        self.price = price

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('item', 'price')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Endpoint to create a new product
@app.route('/product', methods=["POST"])
def add_product():
    item = request.json['item']
    price = request.json['price']

    new_product = Product(item, price)

    db.session.add(new_product)
    db.session.commit()

    product = Product.query.get(new_product.id)

    return product_schema.jsonify(product)

# Endpoint to query all products
@app.route("/products", methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)