from flask import Blueprint, request, url_for, redirect
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from models.category import Category
from models.product import Product

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


class ProductResource(Resource):
    def get(self):
        return redirect(url_for('view.products'))

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('price', type=float, required=True)
        parser.add_argument('category', type=int, required=True)
        parser.add_argument('image', type=str, required=True, regex='^https?://')
        parser.add_argument('description', type=str, required=False)
        parser.add_argument('color', type=str, required=False)
        parser.add_argument('additional_info', type=dict, required=False)
        parser.add_argument('extra_images', type=dict, required=False)
        args = parser.parse_args()

        new_product = Product(**args, price_old=0, promotion=False)
        new_product.commit()
        return new_product, 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('key', type=str, required=True)
        args = parser.parse_args()

        if args['key'] != '123':
            abort(401, message='Unauthorized')

        product = Product.get_product_by_id(args['id'])
        if not product:
            abort(404, message='Product not found')
        product.delete()
        return 'Deleted successfully', 204

    def update_product(self, kwargs, product):
        product.update(**kwargs)
        product.commit()
        return product, 201

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()
        product = Product.get_product_by_id(args['id'])
        if not product:
            abort(404, message='Product not found')

        args = parser.parse_args()
        return self.update_product(args, product)

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()
        product = Product.get_product_by_id(args['id'])
        if not product:
            abort(404, message='Product not found')

        args = parser.parse_args()
        updated_fields = {key: value for key, value in args.items() if value is not None}
        return self.update_product(updated_fields, product)
