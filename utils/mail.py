from flask_mail import Message, Mail
from flask import render_template, session
from flask_login import current_user

mail = Mail()


def send_email(subject, recipients, html_body):
    msg = Message(subject, recipients=recipients)
    msg.html = html_body
    mail.send(msg)
    return "Sent", 200


def send_confirmation_code():
    confirmation_code = session.get('confirmation_code')
    user_email = session.get('confirmation_email')
    subject = "Código de confirmação You Shop"
    recipients = [user_email]
    html_body = render_template("emails/confirmation-code.html", confirmation_code=confirmation_code)
    return send_email(subject, recipients, html_body)
