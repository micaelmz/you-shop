from flask import Blueprint
from controllers.detail_controller import product_detail

detail_blueprint = Blueprint('detail', __name__)

detail_blueprint.route('/id/<int:product_id>', methods=['GET'])(product_detail)
