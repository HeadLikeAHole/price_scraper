from uuid import uuid4
from time import time

from flask import request, url_for

from backend import db
from backend.utils import send_email


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
    current_price = db.Column(db.Boolean)
    desired_price = db.Column(db.Boolean)
    is_monitored = db.Column(db.Boolean, nullable=False, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)


# online store
class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    link = db.Column(db.Text, nullable=False)
    css_class = db.Column(db.String(100))
    products = db.relationship('Product', backref='store', lazy=True)
