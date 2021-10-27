import os


SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')

# remove FSADeprecationWarning from terminal
SQLALCHEMY_TRACK_MODIFICATIONS = False

# show more detailed errors
PROPAGATE_EXCEPTIONS = True

UPLOADED_IMAGES_DEST = os.path.join('backend/static', 'images')

# secret key that will be used for securely signing the session cookie and can be used
# for any other security related needs by extensions or your application
SECRET_KEY = os.environ.get('SECRET_KEY')
