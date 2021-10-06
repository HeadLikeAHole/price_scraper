from datetime import datetime
from flask import send_from_directory
from flask_restful import Resource, reqparse, fields, inputs, marshal_with
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt
)
from . import app, api, db, bcrypt
from .models import User, BlockedToken
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
    help='Password should contain at least one number, one uppercase and one lowercase character, one special symbol and be at least 8 characters long.'
)


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


login_fields = {
    'data': {
        'access_token': fields.String(attribute='data.access_token'),
        'refresh_token': fields.String(attribute='data.refresh_token')
    }
}

login_args = reqparse.RequestParser()
login_args.add_argument('username', type=str, required=True)
login_args.add_argument('password', type=str, required=True)


class Login(Resource):
    @marshal_with(login_fields)
    def post(self):
        args = login_args.parse_args()

        username = args['username']
        password = args['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                'data': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }


class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        now = datetime.now()
        token = BlockedToken(jti=jti, created_at=now)
        db.session.add(token)
        db.session.commit()
        return {'data': {'message': 'Logout successful'}}


class Refresh_Token(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {'data': {'access_token': access_token}}
         

api.add_resource(Users, '/users')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Refresh_Token, '/refresh-token')
