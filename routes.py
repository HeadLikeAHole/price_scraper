from datetime import datetime
from flask import send_from_directory, request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt
)
from . import app, api, db, bcrypt
from .models import User, BlockedToken
from .schemas import UserSchema
from .validators import username_validator, email_validator


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


user_schema = UserSchema()

class Users(Resource):
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


class Login(Resource):
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
