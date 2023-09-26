from flask import render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, login_required, current_user, logout_user
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

from utils.security import calculate_salting_length, validate_recaptcha, generate_6_digit_code
from utils.mail import send_confirmation_code
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

    if not user.is_active:
        flash('Você precisa confirmar seu email antes de fazer login.', 'warning')
        return redirect(url_for('auth.register_validation'))

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

    session['confirmation_code'] = generate_6_digit_code()
    session['confirmation_email'] = new_user.email
    send_confirmation_code()

    flash('Um código de confirmação foi enviado para seu email.', 'success')
    return redirect(url_for('auth.register_validation'))


def register_validation():
    # TODO: em caso não tiver um email na sessão, dar sessão expirada e pedir o email pra mandar um novo codigo -->
    if not session.get('confirmation_code'):
        flash('Você precisa se cadastrar primeiro.', 'warning')
        return redirect(url_for('auth.pre_login'))
    return render_template('validation.html')


def register_validation_post():
    code = request.form.get('code')
    if code == session.get('confirmation_code'):
        user = User.get_by_email(email=session.get('confirmation_email'))
        user.confirm()
        flash('Email confirmado com sucesso.', 'success')
        return redirect(url_for('auth.pre_login'))
    else:
        flash('Código inválido.', 'warning')
        return redirect(url_for('auth.register_validation'))


def logout():
    logout_user()
    return redirect(url_for('home'))
