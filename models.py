from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # is_superuser = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    # products = db.relationship('Product', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class BlockedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     link = db.Column(db.Text, nullable=False)
#     title = db.Column(db.Text)
#     current_price = db.Column(db.Boolean)
#     desired_price = db.Column(db.Boolean)
#     is_monitored = db.Column(db.Boolean, nullable=False, default=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
#
#
# # online store
# class Store(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True, nullable=False)
#     link = db.Column(db.Text, nullable=False)
#     css_class = db.Column(db.String(100))
#     products = db.relationship('Product', backref='store', lazy=True)
