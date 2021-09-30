from flask import send_from_directory
from flask_restful import Resource, reqparse, fields, inputs, marshal_with
from . import app, api, bcrypt, db
from .models import User


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
user_create_args.add_argument('username', type=inputs.regex('^[a-zA-Z0-9]{1, 80}$'), help='Username is required', required=True)
user_create_args.add_argument('email', type=email_validator, help='Email is required', required=True)
user_create_args.add_argument('password', type=password_validator, help='Password is required', required=True)


class Users(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = user_create_args.parse_args()

        username = args['username']
        email = args['email']
        password = args['password']

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

        return {'data': user}, 201


api.add_resource(Users, '/users')
