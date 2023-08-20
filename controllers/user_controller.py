from flask import render_template, redirect, url_for, request
from models.category import Category
from models.user import User
from utils.security import calculate_salting_length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


def login():
    return render_template(
        'login.html',
        form=LoginForm()
    )


def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(email=form.email.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        return redirect(url_for('user.login'))


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Nome', validators=[DataRequired()])
    last_name = StringField('Sobrenome', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[
        DataRequired(),
        validators.Length(min=8, message="A senha deve ter no mínimo 8 caracteres"),
        EqualTo('confirm_password', message='As senhas devem ser iguais')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])


def register():
    return render_template(
        'register.html',
        form=RegistrationForm()
    )


def register_post():
    form = RegistrationForm()
    if form.validate_on_submit():
        password = generate_password_hash(
            password=form.password.data,
            method='pbkdf2:sha256',
            salt_length=calculate_salting_length()
        )
        new_user = User(
            name=form.first_name.data.capitalize(),
            last_name=form.last_name.data.capitalize(),
            email=form.email.data,
            password=password
        )
        new_user.commit()
        return redirect(url_for('user.login'))


def register_validation():
    return render_template('validation.html')


def register_validation_post():
    pass


def logout():
    logout_user()
    return redirect(url_for('home'))


def cart():
    return render_template('cart.html')
