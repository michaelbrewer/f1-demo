dev:
	pip3 install -U pip poetry
	poetry install

test:
	poetry run pytest

clean:
	rm -Rfv cdk.out .pytest_cache cdk/__pycache__ src/f1/__pycache__ tests/__pycache__ tests/functional/__pycache__
	poetry env remove python3

update-requirements:
	poetry export -f requirements.txt --output src/requirements.txt
