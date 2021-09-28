from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create api
app = Flask(__name__, static_url_path='', static_folder='../frontend/build')
app.config.from_pyfile('config.py')

api = Api(app)

# Create database connection object
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from . import routes
