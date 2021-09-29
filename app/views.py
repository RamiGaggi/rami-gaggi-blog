from datetime import datetime

from app import app, db, messages
from app.forms import (
    EditProfileForm,
    EmptyForm,
    LoginForm,
    PostForm,
    RegistrationForm,
    ResetPasswordForm,
    ResetPasswordRequestForm,
)
from app.misc import redirect_to, send_password_reset_email
from app.models import Post, User
from flask import flash, redirect, render_template, request
from flask.helpers import url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False,
    )
    return render_template(
        'index.html',
        title='Explore',
        posts=posts.items,
        pagination=posts,
    )


@app.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect_to('explore')

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False,
    )
    return render_template(
        'index.html',
        title='Home Page',
        form=form,
        posts=posts.items,
        pagination=posts,
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_to('index')

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash(messages.LOGIN_EROOR)
            return redirect_to('login')

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        flash(messages.LOGIN)
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    if current_user.is_anonymous:
        return redirect_to('index')

    logout_user()
    flash(messages.LOGOUT)
    return redirect_to('index')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect_to('index')

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect_to('login')
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    form = EmptyForm()
    user = User.query.filter_by(username=username).first_or_404()  # noqa: WPS442
    page = request.args.get('page', 1, type=int)
    posts = user.posts.paginate(
        page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False,
    )

    return render_template(
        'user.html',
        user=user,
        posts=posts.items,
        form=form,
        pagination=posts,
    )


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect_to('edit_profile')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()  # noqa: WPS442
        if user is None:
            flash(f'User {username} not found.')
            return redirect_to('index')
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect_to('user', username=username)
    return redirect_to('index')


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()  # noqa: WPS442
        if user is None:
            flash('User {username} not found.')
            return redirect_to('index')

        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect_to('user', username=username)

        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.')
        return redirect_to('user', username=username)
    return redirect_to('index')


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # noqa: WPS442
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect_to('login')
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect_to('index')
    user = User.verify_reset_password_token(token)  # noqa: WPS442
    if not user:
        return redirect_to('index')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect_to('login')
    return render_template('reset_password.html', form=form)
