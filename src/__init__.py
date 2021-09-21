from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Create app
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Create database connection object
db = SQLAlchemy(app)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Create app
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Create database connection object
db = SQLAlchemy(app)

from . import routes