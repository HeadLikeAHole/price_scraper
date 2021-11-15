from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from celery import Celery


# without this call "app.config" is empty inside "make_celery" function
load_dotenv()

app = Flask(__name__, static_url_path='', static_folder='../frontend/build')
app.config.from_object('backend.config')

# Create api
api = Api(app)

# Create database connection object
db = SQLAlchemy(app)

# should go after db declaration
ma = Marshmallow(app)

# models should be imported here so they can be detected during migrations
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

from backend.routes import index, products, users
from backend.models import products, users

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = users.BlockedToken.query.filter_by(jti=jti).first()
    return token is not None


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)
