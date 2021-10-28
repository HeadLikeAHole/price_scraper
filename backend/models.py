import os
from time import time
from uuid import uuid4

from flask import request, url_for
import stripe

from backend import db
from backend.utils import send_email


CURRENCY = 'usd'


# products_orders = db.Table(
#     'products_orders',
#     db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
#     db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
# )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60))
    # is_superuser = db.Column(db.Boolean, nullable=False, default=False)
    # products = db.relationship('Product', backref='user', lazy=True)
    registration_confirmation = db.relationship(
        'RegistrationConfirmation',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    @property
    def latest_confirmation(self):
        return self.registration_confirmation.order_by(db.desc(RegistrationConfirmation.expires_at)).first()

    def send_confirmation_email(self):
        # get url root "http://127.0.0.1:5000/" without the last character which is a slash
        link = request.url_root[:-1] + url_for(
            'confirmregistration',
            registration_confirmation_id=self.latest_confirmation.id
        )
        send_email(
            'Registration confirmation',
            f'Please click the link to confirm your registration {link}',
            self.email
        )

    def __repr__(self):
        return f'<User {self.username}>'


class BlockedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class RegistrationConfirmation(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    expires_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id
        self.id = uuid4().hex
        self.expires_at = int(time()) + 1800  # 30 min from now

    @property
    def expired(self):
        return time() > self.expires_at

    def make_expired(self):
        if not self.expired:
            self.expires_at = int(time())


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text)
    current_price = db.Column(db.Integer)
    desired_price = db.Column(db.Integer)
    is_monitored = db.Column(db.Boolean, nullable=False, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)


class OrderedProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)    
    quantity = db.Column(db.Integer)
    product = db.relationship('Product')
    order = db.relationship('Order', back_populates='ordered_products')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    # products = db.relationship('Product', secondary=products_orders, lazy='dynamic')
    ordered_products = db.relationship('OrderedProduct', back_populates='order')

    def set_status(self, new_status):
        self.status = new_status
        db.session.commit()


    def charge_with_stripe(self, token):
        stripe.api = os.environ.get('STRIPE_API_KEY')
        
        return stripe.Charge.create(
            amount=self.amount,  # in cents
            currency=CURRENCY,
            description=self.description,
            source=token
        )

# # online store
# class Store(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True, nullable=False)
#     link = db.Column(db.Text, nullable=False)
#     css_class = db.Column(db.String(100))
#     products = db.relationship('Product', backref='store', lazy=True)
