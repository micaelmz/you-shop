from flask import Blueprint
from controllers.user_controller import pre_login, pre_login_post, register_post, register_validation, \
    register_validation_post, cart, logout, login_post, add_to_cart

user_blueprint = Blueprint('user', __name__)

user_blueprint.route('/login', methods=['GET'])(pre_login)
user_blueprint.route('/login', methods=['POST'])(pre_login_post)
user_blueprint.route('/login/continue', methods=['POST'])(login_post)
user_blueprint.route('/register', methods=['POST'])(register_post)
user_blueprint.route('/register/validation', methods=['GET'])(register_validation)
user_blueprint.route('/register/validation', methods=['POST'])(register_validation_post)
user_blueprint.route('/cart', methods=['GET'])(cart)
user_blueprint.route('/cart/add/<int:product_id>/<int:qnt>', methods=['POST'])(add_to_cart)
user_blueprint.route('/logout', methods=['GET'])(logout)
