install:
	poetry install

run:
	poetry run uvicorn src.main:app --reload

test:
	pytest tests/

lint:
	flake8 src/

format:
	black src/
