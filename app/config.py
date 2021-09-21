import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    DEBUG = os.environ.get('DEBUG') in {'true', 'True', 'TRUE', 1}
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    FLASK_APP = os.environ.get('FLASK_APP')
    SQLALCHEMY_ECHO = DEBUG
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{str(BASE_DIR/"blog.db")}',
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
