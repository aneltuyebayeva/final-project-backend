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

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)