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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)