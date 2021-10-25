from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from oauth import oauth


app = Flask(__name__, static_url_path='', static_folder='../frontend/build')
app.config.from_object('backend.config')

# Create api
api = Api(app)

# Create database connection object
db = SQLAlchemy(app)

# should go after db declaration
ma = Marshmallow(app)

migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

oauth.init_app(app)

from backend import routes, models

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = models.BlockedToken.query.filter_by(jti=jti).first()
    return token is not None
