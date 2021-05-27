from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)
    products = db.relationship('Product', secondary='carts', backref='users')
    orders = db.relationship('Order')
    carts = db.relationship('Cart', backref='carts')
    def to_json(self):
      return {
        "id": self.id,
        "name": self.name,
        "email": self.email
      }

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    address = db.Column(db.String)
    credit_card = db.Column(db.String)
    users = db.relationship('User')
    product_order = db.relationship('Product_Order')
    def to_json(self):
      return {
        "id": self.id,
        "user_id": self.user_id,
        "address": self.address,
        "credit_card": self.credit_card
      }

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    image = db.Column(db.String)
    price = db.Column(db.String)
    carts = db.relationship('Cart')
    orders = db.relationship('Order', secondary='product_orders', backref='products') 
    product_order = db.relationship('Product_Order')
    def to_json(self):
      return {
        "id": self.id,
        "name": self.name,
        "description": self.description,
        "image": self.image,
        "price": self.price
      }
    def to_order_json(self, order_id):
        product_order = Product_Order.query.filter(Product_Order.product_id == self.id, Product_Order.order_id == order_id).first()
        return {
        "id": self.id,
        "name": self.name,
        "description": self.description,
        "image": self.image,
        "price": self.price,
        "quantity": product_order.quantity
      }

class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    products = db.relationship('Product')
    users = db.relationship('User')
    def to_json(self):
      return {
        "id": self.id,
        "product_id": self.product_id,
        "user_id": self.user_id
      }

class Product_Order(db.Model):
    __tablename__ = 'product_orders'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    quantity = db.Column(db.Integer)
    def to_json(self):
      return {
        "id": self.id,
        "product_id": self.product_id,
        "order_id": self.order_id,
        "quantity": self.quantity
      }