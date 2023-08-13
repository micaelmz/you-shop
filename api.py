from flask import Blueprint, request, url_for, redirect, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from models.category import Category
from models.product import Product
from models.review import Review
import json

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


class ProductResource(Resource):
    def get(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': False,
             'help': 'O ID do produto deve ser um inteiro'},
            {'name': 'category_id', 'type': int, 'required': False,
             'help': 'O valor deve ser um ID válido. Em caso de dúvida, consulte a lista de categorias'},
            {'name': 'search', 'type': str, 'required': False}
        ]
        parser = parse_args(args_list)
        args = parser.parse_args()

        if args['id']:
            product = Product.get_product_by_id(args['id'])
            if not product:
                abort(404, message='Produto não encontrado')
            return product.to_dict(properties=True)

        elif args['category_id']:
            products = Product.get_products_by_category_id(args['category_id'])
            if not products:
                abort(404, message='Produto não encontrado para esta categoria')
            return [product.to_dict(properties=True) for product in products]

        elif args['search']:
            products = Product.search_products_by_string(args['search'])
            if not products:
                abort(404, message='Produto não encontrado para esta busca')
            return [product.to_dict(properties=True) for product in products]

    def post(self):
        args_list = [
            {'name': 'name', 'type': str, 'required': True},
            {'name': 'price', 'type': float, 'required': True},
            {'name': 'category_id', 'type': int, 'required': True,
             'help': 'O valor deve ser um ID válido. Em caso de dúvida, consulte a lista de categorias'},
            {'name': 'image', 'type': str, 'required': True,
             'help': 'A imagem deve ser uma URL com extensão válida.'},
            {'name': 'description', 'type': str, 'required': True},
            {'name': 'color', 'type': str, 'required': False},
            {'name': 'additional_info', 'type': dict, 'required': False},
            {'name': 'additional_images', 'type': list, 'location': 'json', 'required': False}
        ]
        parser = parse_args(args_list)
        args = parser.parse_args()

        # todo: fazer algo como new_product = Product(**args, price_old=0, promotion=False)
        new_product = Product(
            name=args['name'],
            price_current=args['price'],
            price_old=0,
            category_id=args['category_id'],
            promotion=False,
            image=args['image'],
            description=args['description'],
            color=args['color'] if args['color'] else Product.detect_color(args['image']),
            additional_info=args['additional_info'],
            additional_images=args['additional_images']
        )
        new_product.commit()

        return new_product.to_dict(), 201

    def put(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': True},
            {'name': 'key', 'type': str, 'required': True},
            {'name': 'name', 'type': str, 'required': True},
            {'name': 'price', 'type': float, 'required': True},
            {'name': 'category_id', 'type': int, 'required': True,
             'help': 'O valor deve ser um ID válido. Em caso de dúvida, consulte a lista de categorias'},
            {'name': 'image', 'type': str, 'required': True,
             'help': 'A imagem deve ser uma URL com extensão válida.'},
            {'name': 'description', 'type': str, 'required': True},
            {'name': 'color', 'type': str, 'required': False},
            {'name': 'additional_info', 'type': dict, 'required': False},
            {'name': 'additional_images', 'type': list, 'location': 'json', 'required': False},
            {'name': 'promotion', 'type': bool, 'required': False}
        ]
        parser = parse_args(args_list)
        args = parser.parse_args()
        check_key(args['key'])

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
            {'name': 'category_id', 'type': int, 'required': False,
             'help': 'O valor deve ser um ID válido. Em caso de dúvida, consulte a lista de categorias'},
            {'name': 'image', 'type': str, 'required': False,
             'help': 'A imagem deve ser uma URL com extensão válida.'},
            {'name': 'description', 'type': str, 'required': False},
            {'name': 'color', 'type': str, 'required': False},
            {'name': 'additional_info', 'type': dict, 'required': False},
            {'name': 'additional_images', 'type': list, 'location': 'json', 'required': False},
            {'name': 'promotion', 'type': bool, 'required': False}
        ]
        parser = parse_args(args_list)
        args = parser.parse_args()
        check_key(args['key'])

        product = Product.get_product_by_id(args['id'])
        if not product:
            abort(404, message='Produto não encontrado')

        args = parser.parse_args()
        updated_fields = {key: value for key, value in args.items() if value is not None}
        return self.update_fields(updated_fields, product)

    def delete(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': True},
            {'name': 'key', 'type': str, 'required': True}
        ]
        parser = parse_args(args_list)
        args = parser.parse_args()
        check_key(args['key'])

        product = Product.get_product_by_id(args['id'])

        if not product:
            abort(404, message='Produto não encontrado')

        product.delete()
        return {'message': 'Produto ID {} deletado com sucesso!'.format(args['id'])}, 200

    @staticmethod
    def update_fields(kwargs: dict, product: Product) -> tuple[dict, int]:
        if not kwargs.get('promotion'):
            kwargs['price_old'] = 0
            kwargs['price_current'] = kwargs['price']
        else:
            kwargs['price_old'] = product.price.new
            kwargs['price_current'] = kwargs['price']

        fields_to_pop = ['key', 'price', 'id']
        for field in fields_to_pop:
            kwargs.pop(field, None)

        product.update(**kwargs)
        product.commit()
        return product.to_dict(properties=True), 201


class CategoryResource(Resource):
    def get(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': False, 'help': 'O ID do produto deve ser um inteiro'},
            {'name': 'name', 'type': str, 'required': False, 'help': 'O nome da categoria deve ser uma string'}
        ]
        parser = parse_args(args_list)
        args = parser.parse_args()

        if args['id']:
            category = Category.get_category_by_id(args['id'])
            if not category:
                abort(404, message='Categoria não encontrada.')
            return category.to_dict()

        elif args['name']:
            category = Category.search_categories_by_name(args['name'])
            if not category:
                abort(404, message='Nenhuma categoria encontrada.')
            return [category.to_dict() for category in category]

        else:
            categories = Category.get_all_categories()
            if not categories:
                abort(404, message='Nenhuma categoria encontrada.')
            return [category.to_dict() for category in categories]

    def post(self):
        args_list = [
            {'name': 'name', 'type': str, 'required': True},
            {'name': 'image', 'type': str, 'required': True, 'help': 'A imagem deve ser uma URL com extensão válida.'}
        ]
        parser = parse_args(args_list)
        args = parser.parse_args()

        new_category = Category(**args)
        new_category.commit()

        return new_category.to_dict(), 201

    def put(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': True},
            {'name': 'key', 'type': str, 'required': True},
            {'name': 'name', 'type': str, 'required': True},
            {'name': 'image', 'type': str, 'required': True,
             'help': 'A imagem deve ser uma URL com extensão válida.'}
        ]
        parser = parse_args(args_list)
        args = parser.parse_args()
        check_key(args['key'])

        category = Category.get_category_by_id(args['id'])
        if not category:
            abort(404, message='Categoria não encontrada')

        return self.update_fields(args, category)


    def patch(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': True},
            {'name': 'key', 'type': str, 'required': True},
            {'name': 'name', 'type': str, 'required': False},
            {'name': 'image', 'type': str, 'required': False,
             'help': 'A imagem deve ser uma URL com extensão válida.'}
        ]
        parser = parse_args(args_list)
        args = parser.parse_args()
        check_key(args['key'])

        category = Category.get_category_by_id(args['id'])
        if not category:
            abort(404, message='Categoria não encontrada')

        args = parser.parse_args()
        updated_fields = {key: value for key, value in args.items() if value is not None}
        return self.update_fields(updated_fields, category)

    def delete(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': True},
            {'name': 'key', 'type': str, 'required': True}
        ]
        parser = parse_args(args_list)
        args = parser.parse_args()
        check_key(args['key'])

        category = Category.get_category_by_id(args['id'])

        if not category:
            abort(404, message='Categoria não encontrada')

        category.delete()
        return {'message': 'Categoria ID {} deletada com sucesso!'.format(args['id'])}, 200

    @staticmethod
    def update_fields(kwargs: dict, category: Category) -> tuple[dict, int]:
        fields_to_pop = ['key', 'id']
        for field in fields_to_pop:
            kwargs.pop(field, None)

        category.update(**kwargs)
        category.commit()
        return category.to_dict(), 201


class ReviewResource(Resource):
    def get(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': False, 'help': 'O ID do produto deve ser um inteiro'},
            {'name': 'author_id', 'type': int, 'required': False, 'help': 'O ID do autor deve ser um inteiro'},
            {'name': 'product_id', 'type': int, 'required': False, 'help': 'O ID do produto deve ser um inteiro'},
            {'name': 'author_name', 'type': bool, 'required': False}
        ]
        parser = parse_args(args_list)
        args = parser.parse_args()

        if args['id']:
            review = Review.get_review_by_id(args['id'])
            if not review:
                abort(404, message='Avaliação não encontrada')

            # Review.to_dict() has a boolean parameter if you want to include the author name
            review_dict = review.to_dict(author_name=args.get('author_name', False))

            return review_dict

        elif args['author_id']:
            reviews = Review.get_reviews_by_author_id(args['author_id'])
            if not reviews:
                abort(404, message='Avaliação não encontrada')
            return [review.to_dict(args.get('author_name', False)) for review in reviews]

        elif args['product_id']:
            reviews = Review.get_reviews_by_product_id(args['product_id'])
            if not reviews:
                abort(404, message='Avaliação não encontrada')
            return [review.to_dict(args.get('author_name', False)) for review in reviews]

    def post(self):
        pass

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass


def parse_args(args: list) -> reqparse.RequestParser:
    parser = reqparse.RequestParser()
    for arg in args:
        parser_args = {
            'name': arg['name'],
            'type': arg['type'],
            'required': arg['required'],
            'help': arg['help'] if 'help' in arg else None
        }
        if 'location' in arg:
            parser_args['location'] = arg['location']
        parser.add_argument(**parser_args)
    return parser


def check_key(key):
    if key != 'verysecretkey':
        abort(401, message='Não autorizado')


api.add_resource(ProductResource, '/api/products')
api.add_resource(CategoryResource, '/api/categories')
api.add_resource(ReviewResource, '/api/reviews')
