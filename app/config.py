import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    DEBUG = os.environ.get('DEBUG') in {'true', 'True', 'TRUE', 1}
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    FLASK_APP = os.environ.get('FLASK_APP')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{str(BASE_DIR/"blog.db")}',
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    RECIPIENTS = os.environ.get('RECIPIENTS', ',').split(',')
