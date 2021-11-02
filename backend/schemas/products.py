from marshmallow import fields
from marshmallow.validate import Length

from backend import ma
from backend.models.products import Product, Store
from backend.translation import get_text as _


class ProductSchema(ma.SQLAlchemyAutoSchema):
	name = fields.Str(validate=Length(min=1, max=200, error=_('invalid_product_title')))
	link = fields.Url(validate=Length(min=1, max=300, error=_('invalid_link_length')))
	desired_price = fields.Int(required=True)
	current_price = fields.Int()
	is_monitored = fields.Boolean()
	user_id = fields.Int()
	store_id = fields.Int()

	class Meta:
		model = Product
		load_instance = True
		dump_only = ('id', 'current_price', 'user_id', 'store_id')


class StoreSchema(ma.SQLAlchemyAutoSchema):
	name = fields.Str(validate=Length(min=1, max=50, error=_('invalid_store_name')))
	link = fields.Url(validate=Length(min=1, max=300, error=_('invalid_link_length')))
	# link = db.Column(db.String(300), nullable=False)
	# css_classes = db.Column(db.Text)
	# products = db.relationship('Product', backref='store', lazy=True)

	class Meta:
		model = Store
		load_instance = True
		dump_only = ('current_price',)