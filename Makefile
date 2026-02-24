run-dev:
	fastapi dev app/main.py

code-formatting:
	black .

test:
	pytest
