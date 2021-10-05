from . import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)
    products = db.relationship('Product', backref='user', lazy=True)

    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user

    @classmethod
    def identity(cls, payload):
        user_id = payload['identity']
        return cls.query.filter_by(id=user_id).first()

    def __repr__(self):
        return f'<User {self.username}>'


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