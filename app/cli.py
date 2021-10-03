import os

import click
from app import app


@app.cli.group()
def translate():
    """Translation and localization commands."""
    pass  # noqa: WPS420


@translate.command()
def update():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o app/translations/messages.pot .;'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i app/translations/messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('app/translations/messages.pot')


@translate.command()
def compile_translation():
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')


@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o app/translations/messages.pot .;'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i app/translations/messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')
