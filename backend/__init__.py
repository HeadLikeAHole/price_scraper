from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


# Create api
api = Api()

# Create database connection object
db = SQLAlchemy()

# should go after db declaration
ma = Marshmallow()

migrate = Migrate()

bcrypt = Bcrypt()

from . import routes, models

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = models.BlockedToken.query.filter_by(jti=jti).first()
    return token is not None


def create_app(config):
    app = Flask(__name__, static_url_path='', static_folder='../frontend/build')
    app.config.from_pyfile(config)

    api.init_app(app)

    db.init_app(app)

    ma.init_app(app)

    migrate.init_app(app, db)

    bcrypt.init_app(app)

    jwt.init_app(app)

    return app