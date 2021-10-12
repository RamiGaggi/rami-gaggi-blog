from app.email import send_email
from flask import current_app, render_template
from flask_babel import _


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        _("[RamiGaggiBlog] Reset Your Password"),
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token),
    )
