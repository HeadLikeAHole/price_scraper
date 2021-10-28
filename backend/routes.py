from collections import Counter
from datetime import datetime
import os
import traceback

from flask import send_from_directory, send_file, request, g, url_for
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
from backend.models import User, BlockedToken, RegistrationConfirmation, Product, OrderedProduct, Order
from backend.schemas import UserSchema, LoginSchema, ImageSchema, OrderSchema
from backend.translation import get_text as _
from backend.image_fns import (
    save_image,
    get_basename,
    get_extension,
    is_extension_allowed,
    get_path,
    find_image_any_format
)
from backend.oauth import vk_oauth


@app.route('/')
def index():
    return send_from_directory('../frontend/build', 'index.html')


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


order_schema = OrderSchema()


class MakeOrder(Resource):
    @staticmethod
    def post():
        data = request.get_json()
        ordered_products = []
        product_id_quantities = Counter(data['product_ids'])

        # "most_common" method converts [1, 1, 2, 3, 5, 5, 5] to [(5, 3), (1, 2), (3, 1), (2, 1)]
        for _id, count in product_id_quantities.most_common():
            product = Product.query.filter_by(id=_id)
            if not product:
                return {'message': _('product_not_found').format(_id)}, 404

            ordered_products.append(OrderedProduct(product_id=_id, quantity=count))

        order = Order(ordered_products=ordered_products, status='pending')
        db.session.add(order)
        db.session.commit()

        order.set_status('failed')
        order.charge_with_stripe(data['token'])
        order.set_status('complete')

        return order_schema.dump(order)


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
api.add_resource(SetNewPassword, '/set-new-password')
api.add_resource(VKLogin, '/login/vk')
api.add_resource(VKAuthorize, '/login/vk/authorized')
api.add_resource(MakeOrder, '/make-order')
