from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# Create api
app = Flask(__name__, static_url_path='', static_folder='frontend/build')
app.config.from_pyfile('config.py')

api = Api(app)

# Create database connection object
db = SQLAlchemy(app)

from . import routes
