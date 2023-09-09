from flask import Blueprint
from controllers.user_controller import cart, cart_add_item, cart_delete_item, cart_update_item

user_blueprint = Blueprint('user', __name__)


user_blueprint.route('/cart', methods=['GET'])(cart)
user_blueprint.route('/cart/add', methods=['POST'])(cart_add_item)
user_blueprint.route('/cart/del', methods=['POST'])(cart_delete_item)
user_blueprint.route('/cart/update', methods=['POST'])(cart_update_item)
