from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import UserMixin, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from utils.security import calculate_salting_length, validate_recaptcha
from controllers.forms import validate_form_or_back, PreLoginForm, LoginForm, RegistrationForm

from models.user import User


def pre_login(continue_modal=None, continue_form=None):
    return render_template(
        'login-register.html',
        form=PreLoginForm(),
        continue_modal=continue_modal,
        continue_form=continue_form
    )


def pre_login_post():
    form = PreLoginForm()
    validate_form_or_back(form)

    user = User.get_by_email(email=form.email.data)

    if user:
        return pre_login(continue_modal='login', continue_form=LoginForm())

    else:
        return pre_login(continue_modal='register', continue_form=RegistrationForm())


def login_post():
    form = LoginForm()
    validate_form_or_back(form)

    if not validate_recaptcha(request.form.get('g-recaptcha-response')):
        flash('Recaptcha inválido.', 'warning')
        return redirect(url_for('auth.pre_login'))

    user = User.get_by_email(email=form.email.data)

    if user and check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember_me.data)
        return redirect(request.form.get('next') or url_for('home'))

    else:
        flash('Email ou senha inválidos.', 'warning')
        return redirect(url_for('auth.pre_login'))


def register_post():
    form = RegistrationForm()
    validate_form_or_back(form)

    if not validate_recaptcha(request.form.get('g-recaptcha-response')):
        flash('Recaptcha inválido.', 'warning')
        return redirect(url_for('auth.pre_login'))

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

    flash('Cadastro realizado com sucesso.', 'success')
    return redirect(url_for('auth.pre_login'))


def register_validation():
    return render_template('validation.html')


def register_validation_post():
    pass


def logout():
    logout_user()
    return redirect(url_for('home'))
