import models
from dotenv import load_dotenv
import os
from flask import Flask, request
from flask_cors import CORS
import sqlalchemy
app = Flask(__name__)
CORS(app)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import jwt

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres', 'postgresql')
models.db.init_app(app)

def root():
  return 'ok'
app.route('/', methods=["GET"])(root)

def create_user():
  try:
    hashed_pw = bcrypt.generate_password_hash(request.json["password"]).decode('utf-8')
    user = models.User(
      name = request.json["name"],
      email = request.json["email"],
      password = hashed_pw
    )
    models.db.session.add(user)
    models.db.session.commit()
    encrypted_id = jwt.encode({"id": user.id}, os.environ.get('JWT_SECRET'), algorithm="HS256")
    return { "user_id": encrypted_id, "user": user.to_json()}
  except sqlalchemy.exc.IntegrityError:
    return { "message": "email is already taken" }, 400
app.route('/users', methods=["POST"])(create_user)


def login_user():
  user = models.User.query.filter_by(email=request.json["email"]).first()
  if not user:
    return { "message": "User not found" }, 404
  if bcrypt.check_password_hash(user.password, request.json["password"]):
    encrypted_id = jwt.encode({"user_id": user.id}, os.environ.get('JWT_SECRET'), algorithm="HS256")
    return { "user_id": encrypted_id, "user": user.to_json() }
  else:
    return { "message": "Invalid password" }, 401
app.route('/users/login', methods = ["POST"])(login_user)


def verify_user():
  decrypted_id = jwt.decode(request.headers["Authorization"], os.environ.get('JWT_SECRET'), algorithms=["HS256"])
  user = models.User.query.filter_by(id=decrypted_id['user_id']).first()
  if not user:
    return { "message": "User not found" }, 404
  return { "user": user.to_json() }
app.route('/users/verify', methods=["GET"])(verify_user)

def seed():
  product1 = models.Product(
    name = "Dream catcher",
    description = "Nice Dream Macrame Dream Catcher Woven Feather Large Wall Hanging Handmade Dreamcatcher Boho Tassels Decoration Home Decor Ornament Craft Gift, 36 x 12 inches (Beige)",
    image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSONoxsW0ANLUyo-Twd2-rtkG2mgn4bOy4Dn9w72jI8fmaH5nmf6WBbBBxtwA&usqp=CAc",
    price = "16.14"
  )
  product2 = models.Product(
    name = "Handmade Quilt",
    description = "King Size Handmade Quilt, Turquoise Bohemian Comforter, Queen Size Quilt, King Size Comforter, Block Print Quilt, Cotton Quilt, Queen Quilt",
    image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmoQeVEA7_sx7SOiCNlcU_yvgaGO3tr93IluJsz0KxoA5UoV4lIN21Wl4c1A&usqp=CAc",
    price = "207.00"
  )
  product3 = models.Product(
    name = "Handmade Patchwork Quilt",
    description = "This 100% cotton patchwork baby/toddler quilt is handmade using highest quality fabric, batting and thread in a traditional “Sunshine and Shadows” pattern.",
    image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQTGGDo0MjYfZDPbJDuuZ794gKQ5dajqIzkpsJnO4BYZreOLM8IRsfevJfixzs&usqp=CAc",
    price = "110.00"
  )
  product4 = models.Product(
    name = "THE PERFECT VINTAGE LEATHER JOURNAL",
    description = "The Vintage Journal is made from 150 GSM Thick and Rustic Paper which makes you feel like you are writing in an old relic. It will hold any ink without any bleed through. The Leather Journal can be used as a Sketchbook, Book of Shadows, Grimoire, Poetry journal, Food journal, spell book, memory journal and many more.",
    image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkV9SijO5487W3KpLT1Cxizk7AfrZ1m15jecFXpe2wTZtVTomMYKq_7sQafRM&usqp=CAc",
    price = "49.95"
  )
  product5 = models.Product(
    name = "Amethyst & Amber Crystal Geode Pillar Candle",
    description = "All Handmade manufacture makes each candle a unique work of art.",
    image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTaWEPkK-E9-bUjHhYy1b0l4v9jKxZI3El27C0eM0Bu_myPXHo-r1Z4E15smL0yxNLpi9yBfNU&usqp=CAc",
    price = "49.00"
  )
  product6 = models.Product(
    name = "Natural Placemats, Boho Placemats",
    description = "Natural Weave multipurpose placemat made from agel root. Feature with hand woven with the local artisan with round design.",
    image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRhv7Hhsld_MKh27-8J5XMfm3GhCCKVyo3sn5FwRavVNqGW9dA3ORNACgwdfQ&usqp=CAc",
    price = "18.00"
  )
  
  models.db.session.add(product1)
  models.db.session.add(product2)
  models.db.session.add(product3)
  models.db.session.add(product4)
  models.db.session.add(product5)
  models.db.session.add(product6)
  models.db.session.commit()
  return "products added"
app.route('/seed', methods=["POST"])(seed)

def create_product():
  product = models.Product(
    name = request.json["name"],
    description = request.json["description"],
    image = request.json["image"],
    price = request.json["price"]
  )
  models.db.session.add(product)
  models.db.session.commit()
  return { "product": product.to_json()}
app.route('/products', methods=["POST"])(create_product)

def all_products():
  products = models.Product.query.all()
  return { "products": [p.to_json() for p in products]}
app.route('/products', methods=["GET"])(all_products)

def single_product(id):
  product = models.Product.query.filter_by(id = id).first()
  return { "product": product.to_json()}
app.route('/products/<int:id>', methods=["GET"])(single_product)

def add_to_cart():
  decrypted_id = jwt.decode(request.headers["Authorization"], os.environ.get('JWT_SECRET'), algorithms=["HS256"])
  user = models.User.query.filter_by(id=decrypted_id['user_id']).first()
  product = models.Product.query.filter_by(id = request.json["product_id"]).first()
  user.products.append(product)
  models.db.session.add(user)
  models.db.session.add(product)
  models.db.session.commit()
  return {
    "user": user.to_json(),
    "product": product.to_json()
  }
app.route('/carts', methods=["POST"])(add_to_cart)

def all_cart_products():
    decrypted_id = jwt.decode(request.headers["Authorization"], os.environ.get('JWT_SECRET'), algorithms=["HS256"])
    user = models.User.query.filter_by(id=decrypted_id['user_id']).first()
    products = user.products
    return {
      "user": user.to_json(),
      "products": [p.to_json() for p in products]
    }
app.route('/carts', methods=["GET"])(all_cart_products)

def remove_from_cart(id):
  decrypted_id = jwt.decode(request.headers["Authorization"], os.environ.get('JWT_SECRET'), algorithms=["HS256"])
  user = models.User.query.filter_by(id=decrypted_id['user_id']).first()
  product = models.Product.query.filter_by(id = id).first()
  user.products.remove(product)
  models.db.session.add(user)
  models.db.session.commit()
  return 'cart is empty'
app.route('/carts/<int:id>', methods=["DELETE"])(remove_from_cart)

def create_order():
  decrypted_id = jwt.decode(request.headers["Authorization"], os.environ.get('JWT_SECRET'), algorithms=["HS256"])
  user = models.User.query.filter_by(id=decrypted_id['user_id']).first()
  order = models.Order(
    address = request.json["address"],
    credit_card = request.json["credit_card"]
  )
  models.db.session.add(order)
  user.orders.append(order)
  models.db.session.add(user)
  models.db.session.commit()
  return {
    "user": user.to_json(),
    "order": order.to_json()
  }
app.route('/orders', methods=["POST"])(create_order)

def create_order_products():
  decrypted_id = jwt.decode(request.headers["Authorization"], os.environ.get('JWT_SECRET'), algorithms=["HS256"])
  user = models.User.query.filter_by(id=decrypted_id['user_id']).first()
  product = models.Product.query.filter_by(id = request.json["product_id"]).first()
  order = models.Order.query.filter_by(id = request.json["order_id"]).first()
  order.products.append(product)
  models.db.session.add(user)
  models.db.session.add(product)
  models.db.session.add(order)
  models.db.session.commit()
  return {
    "user": user.to_json(),
    "product": product.to_json(),
    "order": order.to_json()
  }
app.route('/createorder', methods=["POST"])(create_order_products)

def all_orders():
    decrypted_id = jwt.decode(request.headers["Authorization"], os.environ.get('JWT_SECRET'), algorithms=["HS256"])
    user = models.User.query.filter_by(id=decrypted_id['user_id']).first()
    orders = user.orders
    return {
        "user": user.to_json(),
        "orders": [o.to_json() for o in orders]
    }
app.route('/orders', methods=["GET"])(all_orders)

def single_order(id):
    decrypted_id = jwt.decode(request.headers["Authorization"], os.environ.get('JWT_SECRET'), algorithms=["HS256"])
    user = models.User.query.filter_by(id=decrypted_id['user_id']).first()
    order = models.Order.query.filter_by(id = id).first()
    products = order.products 
    return {
      "user": user.to_json(),
      "order": order.to_json(),
      "products": [p.to_json() for p in products]
    }
app.route('/orders/<int:id>', methods=["GET"])(single_order)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)