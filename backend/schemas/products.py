from marshmallow import fields
from marshmallow.validate import Length

from backend import ma
from backend.models.products import Product, Store
from backend.translation import get_text as _


class ProductSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Product
		# foreign key fields user_id and store_id are not included by default
		include_fk = True
		load_instance = True
		dump_only = ('user_id', 'store_id')


class StoreSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Store
		load_instance = True
