import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from app.config import Config

from flask import Flask, request
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')

mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

babel = Babel(app)

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.core import bp as core_bp
app.register_blueprint(core_bp)

from app import models

if not app.debug:
    if app.config['MAIL_SERVER']:
        
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['RECIPIENTS'],
            subject='Microblog Failure',
            credentials=auth, 
            secure=secure
        )
        
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                   backupCount=10)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'),
)
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('App start...')


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

app.jinja_env.globals['get_locale'] = get_locale
