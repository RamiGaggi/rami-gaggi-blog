install:
	@poetry install;

run:
	@poetry run flask run;

lint:
	@poetry run flake8;

test:
	@poetry run pytest  -s;