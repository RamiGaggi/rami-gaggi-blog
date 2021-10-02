install:
	@poetry install;

shell:
	@poetry run flask shell;

run:
	@poetry run flask run;

lint:
	@poetry run flake8;

test:
	@poetry run pytest  -s;

migrations:
	@poetry run flask db migrate;

migrate: migrations
	@poetry run flask db upgrade;

trans-gen:
	@pybabel extract -F babel.cfg -k _l -o app/translations/messages.pot .;

translate: trans-gen
	@pybabel update -i app/translations/messages.pot -d app/translations -l ru

compile-translation: translate
	@pybabel compile -d app/translations
