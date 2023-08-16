from flask import Blueprint
from flask_restful import Api, Resource, abort
from models.category import Category
from models.product import Product
from models.review import Review
from models.user import User
from utils.api_common import add_arguments, check_key, rename_dict_keys, update_fields, find_or_abort

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


# noinspection PyMethodMayBeStatic
class ProductResource(Resource):
    def get(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': False,
             'help': 'O ID do produto deve ser um inteiro'},
            {'name': 'category_id', 'type': int, 'required': False,
             'help': 'O valor deve ser um ID válido. Em caso de dúvida, solicite a lista de categorias'},
            {'name': 'search', 'type': str, 'required': False}
        ]
        parser = add_arguments(args_list)
        kwargs = parser.parse_args()

        if kwargs['id']:
            product = find_or_abort(Product, id=kwargs['id'], message='Produto não encontrado')
            return product.to_dict_with_selected_properties(['rating']), 200

        elif kwargs['category_id']:
            products = Product.get_products_by_category_id(kwargs['category_id'])
            if not products:
                abort(404, message='Produto não encontrado para esta categoria')
            return [product.to_dict_with_selected_properties(['rating']) for product in products], 200

        elif kwargs['search']:
            products = Product.search_products_by_string(kwargs['search'])
            if not products:
                abort(404, message='Produto não encontrado para esta busca')
            return [product.to_dict_with_selected_properties(['rating']) for product in products], 200

    def post(self):
        args_list = [
            {'name': 'name', 'type': str, 'required': True},
            {'name': 'price', 'type': float, 'required': True},
            {'name': 'category_id', 'type': int, 'required': True,
             'help': 'O valor deve ser um ID válido. Em caso de dúvida, solicite a lista de categorias'},
            {'name': 'image', 'type': str, 'required': True,
             'help': 'A imagem deve ser uma URL com extensão válida.'},
            {'name': 'description', 'type': str, 'required': True},
            {'name': 'color', 'type': str, 'required': False},
            {'name': 'additional_info', 'type': dict, 'required': False},
            {'name': 'additional_images', 'type': list, 'location': 'json', 'required': False}
        ]
        parser = add_arguments(args_list)
        kwargs = parser.parse_args()

        rename_dict_keys(old_dict=kwargs, old_new_keys={'price': 'price_current'})
        kwargs['price_old'] = 0

        new_product = Product(**kwargs)
        new_product.commit()

        return new_product.to_dict_with_selected_properties(['rating']), 201

    def put(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': True},
            {'name': 'key', 'type': str, 'required': True},
            {'name': 'name', 'type': str, 'required': True},
            {'name': 'price', 'type': float, 'required': True},
            {'name': 'category_id', 'type': int, 'required': True,
             'help': 'O valor deve ser um ID válido. Em caso de dúvida, solicite a lista de categorias'},
            {'name': 'image', 'type': str, 'required': True,
             'help': 'A imagem deve ser uma URL com extensão válida.'},
            {'name': 'description', 'type': str, 'required': True},
            {'name': 'color', 'type': str, 'required': False},
            {'name': 'additional_info', 'type': dict, 'required': False},
            {'name': 'additional_images', 'type': list, 'location': 'json', 'required': False},
            {'name': 'on_sale', 'type': bool, 'required': False}
        ]
        parser = add_arguments(args_list)
        kwargs = parser.parse_args()
        check_key(kwargs['key'])

        product = find_or_abort(Product, id=kwargs['id'], message='Produto não encontrado')

        # caso seja uma promoção, o preço antigo é o preço atual e o preço atual é o preço recebido
        if not kwargs.get('on_sale', False):
            kwargs['price_old'] = 0
            rename_dict_keys(kwargs, {'price': 'price_current'})
        else:
            kwargs['price_old'] = product.price.new
            rename_dict_keys(kwargs, {'price': 'price_current'})

        updated_model = update_fields(from_=kwargs, to=product)
        return updated_model.to_dict_with_selected_properties(['rating']), 201

    def patch(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': True},
            {'name': 'key', 'type': str, 'required': True},
            {'name': 'name', 'type': str, 'required': False},
            {'name': 'price', 'type': float, 'required': False},
            {'name': 'category_id', 'type': int, 'required': False,
             'help': 'O valor deve ser um ID válido. Em caso de dúvida, solicite a lista de categorias'},
            {'name': 'image', 'type': str, 'required': False,
             'help': 'A imagem deve ser uma URL com extensão válida.'},
            {'name': 'description', 'type': str, 'required': False},
            {'name': 'color', 'type': str, 'required': False},
            {'name': 'additional_info', 'type': dict, 'required': False},
            {'name': 'additional_images', 'type': list, 'location': 'json', 'required': False},
            {'name': 'on_sale', 'type': bool, 'required': False}
        ]
        parser = add_arguments(args_list)
        kwargs = parser.parse_args()
        check_key(kwargs['key'])

        product = find_or_abort(Product, id=kwargs['id'], message='Produto não encontrado')

        if not kwargs.get('on_sale', False):
            kwargs['price_old'] = 0
            rename_dict_keys(kwargs, {'price': 'price_current'})
        else:
            kwargs['price_old'] = product.price.new
            rename_dict_keys(kwargs, {'price': 'price_current'})

        updated_fields = {key: value for key, value in kwargs.items() if value is not None}
        updated_model = update_fields(from_=updated_fields, to=product)
        return updated_model.to_dict_with_selected_properties(['rating']), 201

    def delete(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': True},
            {'name': 'key', 'type': str, 'required': True}
        ]
        parser = add_arguments(args_list)
        kwargs = parser.parse_args()
        check_key(kwargs['key'])

        product = find_or_abort(Product, id=kwargs['id'], message='Produto não encontrado')
        product.delete()

        return {'message': 'Produto ID {} deletado com sucesso!'.format(kwargs['id'])}, 200


# noinspection PyMethodMayBeStatic
class CategoryResource(Resource):
    def get(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': False, 'help': 'O ID do produto deve ser um inteiro'},
            {'name': 'name', 'type': str, 'required': False, 'help': 'O nome da categoria deve ser uma string'}
        ]
        parser = add_arguments(args_list)
        kwargs = parser.parse_args()

        if kwargs['id']:
            category = find_or_abort(Category, id=kwargs['id'], message='Categoria não encontrada')
            return category.to_dict(), 200

        elif kwargs['name']:
            category = Category.search_by_name(kwargs['name'])
            if not category:
                abort(404, message='Nenhuma categoria encontrada.')
            return [category.to_dict() for category in category], 200

        else:
            categories = Category.get_all()
            if not categories:
                abort(404, message='Nenhuma categoria encontrada.')
            return [category.to_dict() for category in categories], 200

    def post(self):
        args_list = [
            {'name': 'name', 'type': str, 'required': True},
            {'name': 'image', 'type': str, 'required': True, 'help': 'A imagem deve ser uma URL com extensão válida.'}
        ]
        parser = add_arguments(args_list)
        kwargs = parser.parse_args()

        new_category = Category(**kwargs)
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
        parser = add_arguments(args_list)
        kwargs = parser.parse_args()
        check_key(kwargs['key'])

        category = find_or_abort(Category, id=kwargs['id'], message='Categoria não encontrada')

        updated_model = update_fields(from_=kwargs, to=category)
        return updated_model.to_dict(), 201

    def patch(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': True},
            {'name': 'key', 'type': str, 'required': True},
            {'name': 'name', 'type': str, 'required': False},
            {'name': 'image', 'type': str, 'required': False,
             'help': 'A imagem deve ser uma URL com extensão válida.'}
        ]
        parser = add_arguments(args_list)
        kwargs = parser.parse_args()
        check_key(kwargs['key'])

        category = find_or_abort(Category, id=kwargs['id'], message='Categoria não encontrada')

        updated_fields = {key: value for key, value in kwargs.items() if value is not None}
        updated_model = update_fields(from_=updated_fields, to=category)
        return updated_model.to_dict(), 201

    def delete(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': True},
            {'name': 'key', 'type': str, 'required': True}
        ]
        parser = add_arguments(args_list)
        kwargs = parser.parse_args()
        check_key(kwargs['key'])

        category = find_or_abort(Category, id=kwargs['id'], message='Categoria não encontrada')
        category.delete()

        return {'message': 'Categoria ID {} deletada com sucesso!'.format(kwargs['id'])}, 200


# noinspection PyMethodMayBeStatic
class ReviewResource(Resource):
    def get(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': False, 'help': 'O ID do produto deve ser um inteiro'},
            {'name': 'author_id', 'type': int, 'required': False, 'help': 'O ID do autor deve ser um inteiro'},
            {'name': 'product_id', 'type': int, 'required': False, 'help': 'O ID do produto deve ser um inteiro'},
        ]
        parser = add_arguments(args_list)
        kwargs = parser.parse_args()

        if kwargs['id']:
            review = find_or_abort(Review, id=kwargs['id'], message='Avaliação não encontrada')
            return review.to_dict_with_selected_properties(['author_name']), 200

        elif kwargs['author_id']:
            reviews = Review.get_reviews_by_author_id(kwargs['author_id'])
            if not reviews:
                abort(404, message='Avaliação não encontrada')
            return [review.to_dict_with_selected_properties(['author_name']) for review in reviews], 200

        elif kwargs['product_id']:
            reviews = Review.get_reviews_by_product_id(kwargs['product_id'])
            if not reviews:
                abort(404, message='Avaliação não encontrada')
            return [review.to_dict_with_selected_properties(['author_name']) for review in reviews], 200

    def post(self):
        args_list = [
            {'name': 'author_id', 'type': int, 'required': True,
             'help': 'O ID deve ser de um usuário válido. Em caso de dúvida, solicite a lista de usuários'},
            {'name': 'product_id', 'type': int, 'required': True,
             'help': 'O ID deve ser de um produto válido. Em caso de dúvida, solicite a lista de produtos'},
            {'name': 'content', 'type': str, 'required': True},
            {'name': 'review_rating', 'type': float, 'required': True,
             'help': 'O valor deve ser um número entre 0 e 5, com uma casa decimal.'}
        ]
        parser = add_arguments(args_list)
        kwargs = parser.parse_args()

        self.verify_valid_rating(kwargs['review_rating'])
        self.verify_valid_ids(kwargs['author_id'], kwargs['product_id'])

        new_review = Review(**kwargs)
        new_review.commit()

        return new_review.to_dict_with_selected_properties(['author_name']), 201

    def put(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': True,
             'help': 'O ID da avaliação deve ser um inteiro'},
            {'name': 'author_id', 'type': int, 'required': True,
             'help': 'O ID deve ser de um usuário válido. Em caso de dúvida, solicite a lista de usuários'},
            {'name': 'product_id', 'type': int, 'required': True,
             'help': 'O ID deve ser de um produto válido. Em caso de dúvida, solicite a lista de produtos'},
            {'name': 'key', 'type': str, 'required': True},
            {'name': 'content', 'type': str, 'required': True},
            {'name': 'review_rating', 'type': float, 'required': True,
             'help': 'O valor deve ser um número entre 0 e 5, com uma casa decimal.'}
        ]
        parser = add_arguments(args_list)
        kwargs = parser.parse_args()
        check_key(kwargs['key'])

        review = find_or_abort(Review, id=kwargs['id'], message='Avaliação não encontrada')

        # if isn't a valid rating, abort
        self.verify_valid_rating(kwargs['review_rating'])
        self.verify_valid_ids(kwargs['author_id'], kwargs['product_id'])

        updated_model = update_fields(from_=kwargs, to=review)
        return updated_model.to_dict_with_selected_properties(['author_name']), 201

    def patch(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': True,
             'help': 'O ID da avaliação deve ser um inteiro'},
            {'name': 'author_id', 'type': int, 'required': False,
             'help': 'O ID deve ser de um usuário válido. Em caso de dúvida, solicite a lista de usuários'},
            {'name': 'product_id', 'type': int, 'required': False,
             'help': 'O ID deve ser de um produto válido. Em caso de dúvida, solicite a lista de produtos'},
            {'name': 'key', 'type': str, 'required': True},
            {'name': 'content', 'type': str, 'required': False},
            {'name': 'review_rating', 'type': float, 'required': False,
             'help': 'O valor deve ser um número entre 0 e 5, com uma casa decimal.'}
        ]
        parser = add_arguments(args_list)
        kwargs = parser.parse_args()
        check_key(kwargs['key'])

        review = find_or_abort(Review, id=kwargs['id'], message='Avaliação não encontrada')

        self.verify_valid_ids(kwargs.get('author_id'), kwargs.get('product_id'))

        if kwargs.get('review_rating'):
            self.verify_valid_rating(kwargs['review_rating'])

        updated_fields = {key: value for key, value in kwargs.items() if value is not None}
        updated_model = update_fields(from_=updated_fields, to=review)
        return updated_model.to_dict_with_selected_properties(['author_name']), 201

    def delete(self):
        args_list = [
            {'name': 'id', 'type': int, 'required': True},
            {'name': 'key', 'type': str, 'required': True}
        ]
        parser = add_arguments(args_list)
        kwargs = parser.parse_args()
        check_key(kwargs['key'])

        review = find_or_abort(Review, id=kwargs['id'], message='Avaliação não encontrada')
        review.delete()

        return {'message': 'Avaliação ID {} deletada com sucesso!'.format(kwargs['id'])}, 200

    @staticmethod
    def verify_valid_rating(rating: float):
        if rating < 0 or rating > 5:
            abort(400, message='O valor da avaliação deve ser entre 0 e 5, com uma casa decimal.')
        elif rating != 0.5 and rating % 0.5 != 0:
            abort(400, message='O valor da avaliação deve ser entre 0 e 5, com uma casa decimal.')
        return True

    @staticmethod
    def verify_valid_ids(author_id: int = None, product_id: int = None):
        if author_id and not User.get_by_id(author_id):
            abort(404, message='Autor ID {} não encontrado.'.format(author_id))
        elif product_id and not Product.get_by_id(product_id):
            abort(404, message='Produto ID {} não encontrado.'.format(product_id))
        return True


api.add_resource(ProductResource, '/products')
api.add_resource(CategoryResource, 'categories')
api.add_resource(ReviewResource, '/reviews')
