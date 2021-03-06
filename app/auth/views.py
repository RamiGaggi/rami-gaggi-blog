from app import db, messages
from app.auth import bp
from app.auth.email import send_password_reset_email
from app.auth.forms import (
    LoginForm,
    RegistrationForm,
    ResetPasswordForm,
    ResetPasswordRequestForm,
)
from app.models import User
from app.my_utils import redirect_to
from flask import flash, redirect, render_template, request, url_for
from flask_babel import _
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect_to("core.index")

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash(messages.LOGIN_EROOR)
            return redirect_to("auth.login")

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("core.index")

        flash(messages.LOGIN)
        return redirect(next_page)

    return render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    if current_user.is_anonymous:
        return redirect_to("core.index")

    logout_user()
    flash(messages.LOGOUT)
    return redirect_to("core.index")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect_to("core.index")

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(messages.REGISTER)
        return redirect_to("auth.login")
    return render_template("auth/register.html", title=_("Register"), form=form)


@bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # noqa: WPS442
        if user:
            send_password_reset_email(user)
        flash(messages.RESET_PASSWORD_REQUEST)
        return redirect_to("auth.login")
    return render_template(
        "auth/reset_password_request.html", title=_("Reset Password"), form=form
    )


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect_to("core.index")
    user = User.verify_reset_password_token(token)  # noqa: WPS442
    if not user:
        return redirect_to("core.index")
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(messages.RESET_PASSWORD)
        return redirect_to("auth.login")
    return render_template("auth/reset_password.html", form=form)
