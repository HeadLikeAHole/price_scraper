import os


SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')

# stop showing FSADeprecationWarning in the terminal
SQLALCHEMY_TRACK_MODIFICATIONS = False

# show more detailed errors
PROPAGATE_EXCEPTIONS = True

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')