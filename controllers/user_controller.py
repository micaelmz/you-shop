from flask import render_template
from models.category import Category
from models.user import User
from utils.security import calculate_salting_length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length


def login():
    return render_template('login.html')


def login_post():
    pass


def register():
    return render_template('register.html')


def register_post():
    pass


def register_validation():
    return render_template('validation.html')


def register_validation_post():
    pass


def cart():
    return render_template('cart.html')
