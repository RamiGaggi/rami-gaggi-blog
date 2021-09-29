from threading import Thread

from app import app, mail
from flask import redirect, render_template, url_for
from flask_mail import Message
from werkzeug.wrappers import Response


def redirect_to(view, **v_values) -> Response:
    return redirect(url_for(view, **v_values))


def send_async_email(app, msg):  # noqa: WPS442
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        '[RamiGaggiBlog] Reset Your Password',
        sender=app.config['MAIL_USERNAME'],
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt', user=user, token=token),
        html_body=render_template('email/reset_password.html', user=user, token=token),
    )
