from flask import send_from_directory
from flask_restful import Resource, reqparse, fields, inputs, marshal_with
from . import app, api, db
from .models import User
from .validators import username_validator, email_validator


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


user_fields = {
    'data': {
        'id': fields.Integer(attribute='data.id'),
        'username': fields.String(attribute='data.username'),
        'email': fields.String(attribute='data.email')
    }
}


user_create_args = reqparse.RequestParser()
user_create_args.add_argument('username', type=username_validator)
user_create_args.add_argument('email', type=email_validator)
user_create_args.add_argument(
    'password',
    type=inputs.regex(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$'),
    help='Password should contain at least one number, \
    one uppercase and one lowercase character, one special symbol and be at least 8 characters long.'
)


class Users(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = user_create_args.parse_args()

        username = args['username']
        email = args['email']
        password = args['password']

        password_hash = User.hash_password(password)

        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

        return {'data': user}, 201


api.add_resource(Users, '/users')
