from app import app
from app.forms import LoginForm
from flask import flash, redirect, render_template
from flask.helpers import url_for


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Ramil'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!',
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!',
        },
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        is_remember_me = form.remember_me.data
        flash(f'Login requested for user {username}, remember_me={is_remember_me}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
