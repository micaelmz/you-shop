from flask import render_template
from models.category import Category
from models.user import User


def login():
    return render_template('login.html')


def login_post():
    pass


def register():
    return render_template('register.html')


def register_validation():
    return render_template('validation.html')


def register_validation_post():
    pass


def register_post(user: User):
    pass


def cart():
    return render_template('cart.html')
