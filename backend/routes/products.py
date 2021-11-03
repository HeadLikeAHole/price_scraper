from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from backend import api, db
from backend.models.products import Product, Store
from backend.validation import get_data_or_400
from backend.schemas.products import ProductSchema, StoreSchema
from backend.scraper import scrape_price
from backend.utils import extract_store_name


product_schema = ProductSchema()
store_schema = StoreSchema()


class Products(Resource):
    @staticmethod
    @jwt_required()
    def post():
        product = get_data_or_400(product_schema)
        
        current_user = get_jwt_identity()
        product.user_id = current_user

        store_name = extract_store_name(product.url)
        store = Store.query.filter_by(name=store_name).first()

        product.store_id = store.id
        print(product.store_id)

        # db.session.add(user)
        # db.session.commit()

        return product_schema.dump(product), 201


class Stores(Resource):
    @staticmethod
    @jwt_required()
    def post():
        store = get_data_or_400(store_schema)

        db.session.add(store)
        db.session.commit()

        return store_schema.dump(store), 201

        
api.add_resource(Products, '/products')
api.add_resource(Stores, '/stores')