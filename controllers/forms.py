from flask_wtf import FlaskForm
from flask import flash, redirect, url_for
from wtforms import StringField, PasswordField, validators, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


def validate_form_or_back(form: FlaskForm):
    """
    Validates a form and redirects to the previous page with flash messages if it's invalid
    :param form: Form to be validated
    :return:
    """
    if not form.validate_on_submit():
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'warning')
        return redirect(url_for('user.pre_login'))
    return True


class PreLoginForm(FlaskForm):
    """
    Form used to validate the email before login or registration
    """
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='O campo email é obrigatório.'),
            Email(message='O email informado não é válido.')
        ]
    )


class LoginForm(PreLoginForm):
    """
    Form used to validate the email and password before login
    """
    password = PasswordField(
        'Senha',
        validators=[
            DataRequired(message='O campo senha é obrigatório.')
        ]
    )
    remember_me = BooleanField('Manter conectado')


class RegistrationForm(FlaskForm):
    """
    Form used to validate the email, first name, last name and password before registration
    """
    email = StringField(
        'Email', validators=[
            DataRequired(message='O campo email é obrigatório.'),
            Email(message='O email informado não é válido.')
        ])
    first_name = StringField(
        'Nome', validators=[
            DataRequired(message='O campo nome é obrigatório.')
        ])
    last_name = StringField(
        'Sobrenome', validators=[
            DataRequired(message='O campo sobrenome é obrigatório.')
        ])
    password = PasswordField(
        'Senha', validators=[
            DataRequired(message='O campo senha é obrigatório.'),
            validators.Length(min=8, message="A senha deve ter no mínimo 8 caracteres"),
            EqualTo('confirm_password', message='As senhas devem ser iguais')
        ])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(message='O campo confirmar senha é obrigatório.')
        ])
