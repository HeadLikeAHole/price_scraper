from backend import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(300), nullable=False)
    desired_price = db.Column(db.Integer, nullable=False)
    current_price = db.Column(db.Integer)
    is_monitored = db.Column(db.Boolean, nullable=False, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)


# online store
class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    url = db.Column(db.String(300), nullable=False)
    css_classes = db.Column(db.Text)
    products = db.relationship('Product', backref='store', lazy=True)
