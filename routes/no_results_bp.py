from flask import Blueprint
from controllers.no_results_controller import product, category, search

no_results_blueprint = Blueprint('no_results', __name__)

no_results_blueprint.route('/product/<int:product_id>', methods=['GET'])(product)
no_results_blueprint.route('/category/<int:category_id>', methods=['GET'])(category)
no_results_blueprint.route('/search/<string:search_query>', methods=['GET'])(search)
