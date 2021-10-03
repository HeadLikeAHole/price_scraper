import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt import JWT


load_dotenv()

app = Flask(__name__, static_url_path='', static_folder='../frontend/build')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
# remove FSADeprecationWarning from terminal
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('APP_SECRET_KEY')

# Create api
api = Api(app)

# Create database connection object
db = SQLAlchemy(app)

migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

from . import routes, models

jwt = JWT(app, models.User.authenticate, models.User.identity)
