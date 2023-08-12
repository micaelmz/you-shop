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
        args_list = [
            {'name': 'id', 'type': int, 'required': False, 'help': 'O ID do produto deve ser um inteiro'},
            {'name': 'category', 'type': int, 'required': False,
             'help': 'O valor deve ser um ID válido. Em caso de dúvida, consulte a lista de categorias'},
            {'name': 'search', 'type': str, 'required': False}
        ]
        self.parse_args(args_list)
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
        args_list = [
                {'name': 'name', 'type': str, 'required': True},
                {'name': 'price', 'type': float, 'required': True},
                {'name': 'category', 'type': int, 'required': True,
                 'help': 'O valor deve ser um ID válido. Em caso de dúvida, consulte a lista de categorias'},
                {'name': 'image', 'type': str, 'required': True,
                 'help': 'A imagem deve ser uma URL com extensão válida.'},
                {'name': 'description', 'type': str, 'required': False},
                {'name': 'color', 'type': str, 'required': False},
                {'name': 'additional_info', 'type': dict, 'required': False},
                {'name': 'extra_images', 'type': list, 'location': 'json', 'required': False}
            ]
        self.parse_args(args_list)
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
        args_list = [
            {'name': 'id', 'type': int, 'required': True},
            {'name': 'key', 'type': str, 'required': True}
        ]
        self.parse_args(args_list)
        args = parser.parse_args()

        self.check_key(args['key'])

        product = Product.get_product_by_id(args['id'])

        if not product:
            abort(404, message='Product not found')

        product.delete()
        return {'message': 'Produto deletado com sucesso!'}, 200

    def put(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': True},
            {'name': 'key', 'type': str, 'required': True},
            {'name': 'name', 'type': str, 'required': True},
            {'name': 'price', 'type': float, 'required': True},
            {'name': 'category', 'type': int, 'required': True,
             'help': 'O valor deve ser um ID válido. Em caso de dúvida, consulte a lista de categorias'},
            {'name': 'image', 'type': str, 'required': True, 'help': 'A imagem deve ser uma URL com extensão válida.'},
            {'name': 'description', 'type': str, 'required': False},
            {'name': 'color', 'type': str, 'required': False},
            {'name': 'additional_info', 'type': dict, 'required': False},
            {'name': 'extra_images', 'type': list, 'location': 'json', 'required': False},
            {'name': 'promotion', 'type': bool, 'required': False}
        ]
        self.parse_args(args_list)
        args = parser.parse_args()
        self.check_key(args['key'])

        product = Product.get_product_by_id(args['id'])
        if not product:
            abort(404, message='Product not found')

        return self.update_fields(args, product)

    def patch(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': True},
            {'name': 'key', 'type': str, 'required': True},
            {'name': 'name', 'type': str, 'required': False},
            {'name': 'price', 'type': float, 'required': False},
            {'name': 'category', 'type': int, 'required': False,
             'help': 'O valor deve ser um ID válido. Em caso de dúvida, consulte a lista de categorias'},
            {'name': 'image', 'type': str, 'required': False,
             'help': 'A imagem deve ser uma URL com extensão válida.'},
            {'name': 'description', 'type': str, 'required': False},
            {'name': 'color', 'type': str, 'required': False},
            {'name': 'additional_info', 'type': dict, 'required': False},
            {'name': 'extra_images', 'type': list, 'location': 'json', 'required': False},
            {'name': 'promotion', 'type': bool, 'required': False}
        ]
        self.parse_args(args_list)
        args = parser.parse_args()

        product = Product.get_product_by_id(args['id'])
        if not product:
            abort(404, message='Product not found')

        args = parser.parse_args()
        updated_fields = {key: value for key, value in args.items() if value is not None}
        return self.update_fields(updated_fields, product)

    @staticmethod
    def parse_args(args_list):
        for arg in args_list:
            parser.add_argument(arg['name'], type=arg['type'], required=arg['required'],
                                help=arg['help'] if 'help' in arg else None)

    @staticmethod
    def update_fields(kwargs, product):
        if not kwargs.get('promotion'):
            kwargs['price_old'] = 0
            kwargs['price_current'] = kwargs['price']
        else:
            kwargs['price_old'] = product.price.new
            kwargs['price_current'] = kwargs['price']

        kwargs['image_thumb'] = kwargs['image']
        fields_to_pop = ['key', 'price', 'image', 'id']
        for field in fields_to_pop:
            kwargs.pop(field, None)

        product.update(**kwargs)
        product.commit()
        return product.to_dict(), 201

    @staticmethod
    def check_key(key):
        if key != 'verysecretkey':
            abort(401, message='Não autorizado')


api.add_resource(ProductResource, '/api/products')
