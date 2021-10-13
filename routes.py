from datetime import datetime
from flask import send_from_directory
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt
)
from . import app, api, db, bcrypt
from .validation import get_data_or_400
from .models import User, BlockedToken, UserConfirmation
from .schemas import UserSchema, LoginSchema


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


class Users(Resource):
    def post(self):
        user_schema = UserSchema()

        user = get_data_or_400(user_schema)

        # hash password
        user.password = bcrypt.generate_password_hash(user.password).decode('utf-8')

        db.session.add(user)
        db.session.commit()

        user_confirmation = UserConfirmation(user.id)
        db.session.add(user_confirmation)
        db.session.commit()

        user.send_confirmation_email()

        return user_schema.dump(user), 201


class Login(Resource):
    def post(self):
        login_schema = LoginSchema()

        data = get_data_or_400(login_schema)

        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            user_confirmation = user.latest_confirmation
            if user_confirmation and user_confirmation.confirmed:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)

                return {'access_token': access_token, 'refresh_token': refresh_token}

            return {'error': 'You have not confirmed registration. Please check your email.'}, 400


class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        now = datetime.now()
        token = BlockedToken(jti=jti, created_at=now)
        db.session.add(token)
        db.session.commit()
        return {'message': 'Logout successful'}


class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return {'access_token': access_token}


class ConfirmUser(Resource):
    def get(self, user_confirmation_id):
        user_confirmation = UserConfirmation.query.filter_by(id=user_confirmation_id).first()

        if not user_confirmation:
            return {'message': 'Confirmation reference not found'}, 404

        if user_confirmation.expired:
            return {'message': 'The link has expired'}, 400

        if user_confirmation.confirmed:
            return {'message': 'Registration has already been confirmed'}, 400

        user_confirmation.confirmed = True
        db.session.commit()

        return {'message': 'User confirmation successful'}


class ConfirmUserByUser(Resource):
    def post(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {'message': 'User not found'}, 404

        user_confirmation = user.latest_confirmation()
        if user_confirmation:
            if user_confirmation.confirmed:
                return {'message': 'User has already been confirmed'}, 400
            user_confirmation.make_expired()
            db.session.commit()

        new_confirmation = UserConfirmation(user_id)
        db.session.add(new_confirmation)
        db.session.commit()
        user.send_confirmation_email()

        return {'message': 'Confirmation email has been sent'}, 201


api.add_resource(Users, '/users')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(RefreshToken, '/refresh-token')
api.add_resource(ConfirmUser, '/confirm-user/<string:user_confirmation_id>')
api.add_resource(ConfirmUserByUser, '/confirm-user-by-user/<int:user_id>')
