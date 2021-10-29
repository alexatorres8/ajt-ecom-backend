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

# Items
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __init__(self, title, price, image, description):
        self.title = title
        self.price = price
        self.image = image
        self.description = description

class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'price', 'image', 'description')

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

# Endpoint to create a new item
@app.route('/item', methods=["POST"])
def add_item():
    title = request.json['title']
    price = request.json['price']
    image = request.json['image']
    description = request.json['description']

    new_item = Item(title, price, image, description)

    db.session.add(new_item)
    db.session.commit()

    item = Item.query.get(new_item.id)

    return item_schema.jsonify(item)

# Endpoint to query all items
@app.route("/items", methods=["GET"])
def get_items():
    all_items = Item.query.all()
    result = items_schema.dump(all_items)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)