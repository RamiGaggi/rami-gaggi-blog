from datetime import datetime

from app import app, db, messages
from app.forms import EditProfileForm, EmptyForm, PostForm
from app.models import Post, User
from app.my_utils import redirect_to
from app.translate import translate
from flask import flash, jsonify, redirect, render_template, request
from flask.helpers import url_for
from flask_babel import _
from flask_login import current_user, login_required
from langdetect import LangDetectException, detect


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
        title=_('All posts'),
        posts=posts.items,
        pagination=posts,
    )


@app.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    form = PostForm()
    if form.validate_on_submit():
        try:
            language = detect(form.post.data)
        except LangDetectException:
            language = ''
        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect_to('explore')

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False,
    )
    return render_template(
        'index.html',
        title=_('My feed'),
        form=form,
        posts=posts.items,
        pagination=posts,
    )


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
        flash(messages.EDIT_PROFILE)
        return redirect_to('edit_profile')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()  # noqa: WPS442
        if user is None:
            flash(messages.USERNAME_NOT_FOUND(username))
            return redirect_to('index')
        if user == current_user:
            flash(messages.FOLLOW_YOURSELF)
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(messages.FOLLOW(username))
        return redirect_to('user', username=username)
    return redirect_to('index')


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()  # noqa: WPS442
        if user is None:
            flash(messages.USERNAME_NOT_FOUND(username))
            return redirect_to('index')

        if user == current_user:
            flash(messages.UNFOLLOW_YOURSELF)
            return redirect_to('user', username=username)

        current_user.unfollow(user)
        db.session.commit()
        flash(messages.UNFOLLOW(username))
        return redirect_to('user', username=username)
    return redirect_to('index')


@app.route('/translate', methods=['POST'])
def translate_text():
    app.logger.info(request)
    return jsonify(
        {
            'text': translate(
                request.form['text'],
                request.form['source_language'],
                request.form['dest_language'],
            ),
        },
    )
