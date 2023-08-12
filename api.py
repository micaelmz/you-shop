from flask import Blueprint, request, url_for, redirect, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from models.category import Category
from models.product import Product
import json

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)
parser = reqparse.RequestParser()


class ProductResource(Resource):
    def get(self):
        parser.add_argument('id', type=int, required=False,
                            help='O ID do produto deve ser um inteiro')
        parser.add_argument('category', type=int, required=False,
                            help='O valor deve ser um ID válido. Em caso de dúvida, consulte a lista de categorias')
        parser.add_argument('search', type=str, required=False)
        args = parser.parse_args()

        if args['id']:
            product = Product.get_product_by_id(args['id'])
            if not product:
                abort(404, message='Produto não encontrado')
            return product.to_dict()

        elif args['category']:
            products = Product.get_products_by_category_id(args['category'])
            if not products:
                abort(404, message='Produto não encontrado para esta categoria')
            return [product.to_dict() for product in products]

        elif args['search']:
            products = Product.search_products_by_string(args['search'])
            if not products:
                abort(404, message='Produto não encontrado para esta busca')
            return [product.to_dict() for product in products]

    def post(self):
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('price', type=float, required=True)
        parser.add_argument('category', type=int, required=True,
                            help='O valor deve ser um ID válido. Em caso de dúvida, consulte a lista de categorias')
        parser.add_argument('image', type=str, required=True,
                            help='A imagem deve ser uma URL com extensão válida.')  # todo: validar se é uma url e se é uma imagem (jpg, png)
        parser.add_argument('description', type=str, required=False)
        parser.add_argument('color', type=str, required=False)
        parser.add_argument('additional_info', type=dict, required=False)
        parser.add_argument('extra_images', type=list, location='json', required=False)
        args = parser.parse_args()

        # new_product = Product(**args, price_old=0, promotion=False)
        new_product = Product(
            name=args['name'],
            price_current=args['price'],
            price_old=0,
            category=args['category'],
            promotion=False,
            image_thumb=args['image'],
            description=args['description'],
            color=args['color'] if args['color'] else Product.detect_color(args['image']),
            additional_info=args['additional_info'],
            extra_images=args['extra_images']
        )
        new_product.commit()

        return new_product.to_dict(), 201

    def delete(self):
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('key', type=str, required=True)
        args = parser.parse_args()

        if args['key'] != '123':
            abort(401, message='Não autorizado')

        product = Product.get_product_by_id(args['id'])

        if not product:
            abort(404, message='Product not found')

        product.delete()
        return {'message': 'Produto deletado com sucesso!'}, 200

    def update_product(self, kwargs, product):
        product.update(**kwargs)
        product.commit()
        return product, 201

    def put(self):
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()
        product = Product.get_product_by_id(args['id'])
        if not product:
            abort(404, message='Product not found')

        args = parser.parse_args()
        return self.update_product(args, product)

    def patch(self):
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()
        product = Product.get_product_by_id(args['id'])
        if not product:
            abort(404, message='Product not found')

        args = parser.parse_args()
        updated_fields = {key: value for key, value in args.items() if value is not None}
        return self.update_product(updated_fields, product)


api.add_resource(ProductResource, '/api/products')
