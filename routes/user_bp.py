from flask import Blueprint
from controllers.user_controller import login, login_post, register, register_post, register_validation, \
    register_validation_post, cart, logout

user_blueprint = Blueprint('user', __name__)

user_blueprint.route('/login', methods=['GET'])(login)
user_blueprint.route('/login', methods=['POST'])(login_post)
user_blueprint.route('/register', methods=['GET'])(register)
user_blueprint.route('/register', methods=['POST'])(register_post)
user_blueprint.route('/register/validation', methods=['GET'])(register_validation)
user_blueprint.route('/register/validation', methods=['POST'])(register_validation_post)
user_blueprint.route('/cart', methods=['GET'])(cart)
user_blueprint.route('/logout', methods=['GET'])(logout)
