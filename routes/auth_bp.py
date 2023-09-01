from flask import Blueprint
from controllers.auth_controller import pre_login, pre_login_post, register_post, register_validation, \
    register_validation_post, logout, login_post

auth_blueprint = Blueprint('auth', __name__)


auth_blueprint.route('/login', methods=['GET'])(pre_login)
auth_blueprint.route('/login', methods=['POST'])(pre_login_post)
auth_blueprint.route('/login/continue', methods=['POST'])(login_post)
auth_blueprint.route('/register', methods=['POST'])(register_post)
auth_blueprint.route('/register/validation', methods=['GET'])(register_validation)
auth_blueprint.route('/register/validation', methods=['POST'])(register_validation_post)
auth_blueprint.route('/logout', methods=['GET'])(logout)
