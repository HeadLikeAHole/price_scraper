from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from backend import api
from backend.models.products import Product, Store
from backend.validation import get_data_or_400
from backend.schemas.products import ProductSchema
from backend.scraper import scrape_price


product_schema = ProductSchema()


class Products(Resource):
    @staticmethod
    @jwt_required()
    def post():
        product = get_data_or_400(product_schema)

        # product.current_price = scrape_price()

        current_user = get_jwt_identity()
        product.user_id = current_user

        # store_name = extract_store_name(url)

        # db.session.add(user)
        # db.session.commit()

        return product_schema.dump(product), 201


api.add_resource(Products, '/products')
