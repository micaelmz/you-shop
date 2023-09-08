from flask import Blueprint
from controllers.product_controller import all_products, products_by_category, search_page, search_form, search_products, product_detail

product_blueprint = Blueprint('product', __name__)

product_blueprint.route('/all', methods=['GET'])(all_products)
product_blueprint.route('/category/<int:category_id>', methods=['GET'])(products_by_category)
product_blueprint.route('/search', methods=['GET'])(search_page)
product_blueprint.route('/search', methods=['POST'])(search_form)
product_blueprint.route('/search/<string:search_query>', methods=['GET'])(search_products)
product_blueprint.route('/id/<int:product_id>', methods=['GET'])(product_detail)
