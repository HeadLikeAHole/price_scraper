import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_uploads import configure_uploads, patch_request_class

from backend.image_fns import IMAGE_SET

# without this path '.../price_scraper' specified as 'root_path'
# 'send_file' function can't locate static files when it receives absolute path as argument
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, root_path=ROOT_PATH)
app.config.from_object('backend.config')

'''
in the library file flask_uploads.py the import:
    from werkzeug import secure_filename, FileStorage
should be replaced with:
    from werkzeug.datastructures import FileStorage
    from werkzeug.utils import secure_filename
'''
# set maximum image size 1MB
patch_request_class(app, 1024 * 1024)
# connect uploads to the app
# UPLOADED_IMAGES_DEST should be added to app config
configure_uploads(app, IMAGE_SET)

# Create api
api = Api(app)

# Create database connection object
db = SQLAlchemy(app)

# should go after db declaration
ma = Marshmallow(app)

migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

from backend import routes, models

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = models.BlockedToken.query.filter_by(jti=jti).first()
    return token is not None
