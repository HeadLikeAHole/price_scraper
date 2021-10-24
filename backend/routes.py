from datetime import datetime
import os
import traceback

from flask import send_from_directory, request, send_file
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt
)
from flask_uploads import UploadNotAllowed

from backend import app, api, db, bcrypt
from backend.validation import get_data_or_400
from backend.models import User, BlockedToken, RegistrationConfirmation
from backend.schemas import UserSchema, LoginSchema, ImageSchema
from backend.translation import get_text as _
from backend.image_fns import (
    save_image,
    get_basename,
    get_extension,
    is_extension_allowed,
    get_path,
    find_image_any_format
)


@app.route('/')
def index():
    return send_from_directory('../frontend/build', 'index.html')


class Users(Resource):
    def post(self):
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
    def post(self):
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
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        now = datetime.now()
        token = BlockedToken(jti=jti, created_at=now)
        db.session.add(token)
        db.session.commit()
        return {'message': _('logout_success')}


class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return {'access_token': access_token}


class ConfirmRegistration(Resource):
    def get(self, registration_confirmation_id):
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
    def post(self, user_id):
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


image_schema = ImageSchema()


class ImageUpload(Resource):
    @jwt_required()
    def post(self):
        # request.files is a dict {'image': FileStorage}
        # "image" key is required because it's a field in the schema
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f'user_{user_id}'

        try:
            image_path = save_image(data['image'], folder)
            basename = get_basename(image_path)
            return {'message': _('image_uploaded').format(basename)}, 201
        except UploadNotAllowed:
            extension = get_extension(data['image'])
            return {'message': _('invalid_image_ext').format(extension)}, 400


class Image(Resource):
    @jwt_required()
    def get(self, filename):
        user_id = get_jwt_identity()
        folder = f'user_{user_id}'

        if not is_extension_allowed(filename):
            extension = get_extension(filename)
            return {'message': _('invalid_image_ext').format(extension)}, 400
        try:
            return send_file(get_path(filename, folder))
        except FileNotFoundError:
            return {'message': _('image_not_found').format(filename)}, 404

    @jwt_required()
    def delete(self, filename):
        user_id = get_jwt_identity()
        folder = f'user_{user_id}'

        if not is_extension_allowed(filename):
            extension = get_extension(filename)
            return {'message': _('invalid_image_ext').format(extension)}, 400
        try:
            os.remove(get_path(filename, folder))
            return {'message': _('image_deleted').format(filename)}, 200
        except FileNotFoundError:
            traceback.print_exc()
            return {'message': _('image_delete_failed').format(filename)}, 500


class AvatarUpload(Resource):
    @jwt_required()
    def put(self):
        data = image_schema.load(request.files)
        filename = f'user_{get_jwt_identity()}'
        folder = 'avatars'

        avatar_path = find_image_any_format(filename, folder)
        if avatar_path:
            try:
                os.remove(avatar_path)
            except:
                return {'message': _('avatar_delete_failed')}, 500

        try:
            extension = get_extension(data['image'].filename)
            avatar = filename + extension
            avatar_path = save_image(data['image'], folder, avatar)
            basename = get_basename(avatar_path)
            return {'message': _('image_uploaded').format(basename)}, 201
        except UploadNotAllowed:
            extension = get_extension(data['image'])
            return {'message': _('invalid_image_ext').format(extension)}, 400


class Avatar(Resource):
    @jwt_required()
    def get(self, user_id):
        filename = f'user_{user_id}'
        folder = 'avatars'

        avatar_path = find_image_any_format(filename, folder)
        if avatar_path:
            return send_file(avatar_path)

        return {'message': _('avatar_not_found')}, 404


api.add_resource(Users, '/users')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(RefreshToken, '/refresh-token')
api.add_resource(ConfirmRegistration, '/confirm-registration/<string:registration_confirmation_id>')
api.add_resource(ConfirmRegistrationByUser, '/confirm-registration-by-user/<int:user_id>')
api.add_resource(ImageUpload, '/upload/image')
api.add_resource(Image, '/image/<string:filename>')
api.add_resource(AvatarUpload, '/upload/avatar')
api.add_resource(Avatar, '/avatar/<int:user_id>')
