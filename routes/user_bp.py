from flask import Blueprint
from controllers.user_controller import cart, add_to_cart, delete_item

user_blueprint = Blueprint('user', __name__)


user_blueprint.route('/cart', methods=['GET'])(cart)
user_blueprint.route('/cart/add', methods=['POST'])(add_to_cart)
user_blueprint.route('/cart/del', methods=['POST'])(delete_item)

