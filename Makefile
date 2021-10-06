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

update-translation:
	@poetry run flask translate update;

compile-translation: update-translation
	@poetry run flask translate compile-translation;
