from datetime import datetime

from flask import send_from_directory, g, request, url_for
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt
)

from backend import app, api, db, bcrypt
from backend.validation import get_data_or_400
from backend.models import User, BlockedToken, RegistrationConfirmation
from backend.schemas import UserSchema, LoginSchema
from backend.translation import get_text as _
from backend.oauth import vk_oauth


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


class Users(Resource):
    @staticmethod
    def post():
        user_schema = UserSchema()

        user = get_data_or_400(user_schema)

        # hash password
        user.password = bcrypt.generate_password_hash(user.password).decode('utf-8')

        db.session.add(user)
        db.session.commit()

        registration_confirmation = RegistrationConfirmation(user.id)
        db.session.add(registration_confirmation)
        db.session.commit()

        user.send_confirmation_email()

        return user_schema.dump(user), 201


class Login(Resource):
    @staticmethod
    def post():
        login_schema = LoginSchema()

        data = get_data_or_400(login_schema)

        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            registration_confirmation = user.latest_confirmation
            if registration_confirmation and registration_confirmation.confirmed:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)

                return {'access_token': access_token, 'refresh_token': refresh_token}

            return {'error': _('registration_not_confirmed')}, 400


class Logout(Resource):
    @staticmethod
    @jwt_required()
    def post():
        jti = get_jwt()['jti']
        now = datetime.now()
        token = BlockedToken(jti=jti, created_at=now)
        db.session.add(token)
        db.session.commit()
        return {'message': _('logout_success')}


class RefreshToken(Resource):
    @staticmethod
    @jwt_required(refresh=True)
    def post():
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return {'access_token': access_token}


class ConfirmRegistration(Resource):
    @staticmethod
    def get(registration_confirmation_id):
        registration_confirmation = RegistrationConfirmation.query.filter_by(id=registration_confirmation_id).first()

        if not registration_confirmation:
            return {'message': _('registration_confirmation_not_found')}, 404

        if registration_confirmation.expired:
            return {'message': _('link_expired')}, 400

        if registration_confirmation.confirmed:
            return {'message': _('registration_already_confirmed')}, 400

        registration_confirmation.confirmed = True
        db.session.commit()

        return {'message': _('registration_confirmation_success')}


class ConfirmRegistrationByUser(Resource):
    @staticmethod
    def post(user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {'message': _('user_not_found')}, 404

        registration_confirmation = user.latest_confirmation()
        if registration_confirmation:
            if registration_confirmation.confirmed:
                return {'message': _('registration_already_confirmed')}, 400
            registration_confirmation.make_expired()
            db.session.commit()

        new_confirmation = RegistrationConfirmation(user_id)
        db.session.add(new_confirmation)
        db.session.commit()
        user.send_confirmation_email()

        return {'message': _('registration_confirmation_email_sent')}, 201


class SetNewPassword(Resource):
    @staticmethod
    @jwt_required(fresh=True)
    def post():
        login_schema = LoginSchema()

        data = get_data_or_400(login_schema)

        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user:
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
            db.session.commit()
            return {'message': _('password_updated')}, 201

        return {'error': _('user_not_found')}, 404


class VKLogin(Resource):
    @staticmethod
    def get():
        return vk_oauth.authorize(callback=url_for('vkauthorize', _external=True))


class VKAuthorize(Resource):
    @staticmethod
    def get():
        resp = vk_oauth.authorized_response()

        if resp is None or resp['user_id'] is None:
            error_response = {
                'error': request.args['error'],
                'error_description': request.args['error_description']
            }
            return error_response

        user_id = str(resp['user_id'])
        
        # get user info
        # g.access_token = resp['access_token']
        # vk_user = vk_oauth.get('users.get?v=5.131')
        # vk_user_id = vk_user.data['response'][0]['id']

        user = User.query.filter_by(username=user_id).first()

        if not user:
            user = User(username=user_id)
            db.session.add(user)
            db.session.commit()

            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {'access_token': access_token, 'refresh_token': refresh_token}


api.add_resource(Users, '/users')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(RefreshToken, '/refresh-token')
api.add_resource(ConfirmRegistration, '/confirm-registration/<string:registration_confirmation_id>')
api.add_resource(ConfirmRegistrationByUser, '/confirm-registration-by-user/<int:user_id>')
api.add_resource(SetNewPassword, '/set-new-password')
api.add_resource(VKLogin, '/login/vk')
api.add_resource(VKAuthorize, '/login/vk/authorized')
