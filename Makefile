run-dev:
	fastapi dev app/main.py

code-formatting:
	black .

test:
	pytest

migrate:
	alembic upgrade head

install-dependencies:
	pip install -r requirements.txt

install-dependencies-dev:
	pip install -r requirements.dev.txt
