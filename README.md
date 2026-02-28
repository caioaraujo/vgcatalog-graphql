# vgcatalog-graphql

[!WARNING]
Project under construction.

The goal of this project is to provide CRUD operations based on Video Game titles, provided by an API using GraphQL.

This project is using:
- [FastAPI](https://fastapi.tiangolo.com/) to provide the API;
- [SQLAlchemy](https://www.sqlalchemy.org/) ver. 2 for database interactions;
- [alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations;
- [psycopg2](https://pypi.org/project/psycopg2/) as PostgreSQL client;
- [pytest](https://pypi.org/project/pytest/) + [pytest-postgresql](https://pypi.org/project/pytest-postgresql/) for tests;
- [pytest-cov](https://pypi.org/project/pytest-cov/) for tests coverage;
- [factory_boy](https://factoryboy.readthedocs.io/) to provide models fixtures for tests;
- [black](https://pypi.org/project/black/) for code formatting.

## Requirements

- Python 3.14+
- PostgreSQL

All Python dependencies are listed on `requirements.txt` in the project root.

Ex: `pip install -r requirements.txt`

NOTE: Consider to [create and activate a virtual environment](https://docs.python.org/3/library/venv.html) to install
all the dependencies.

## Setup and Running

### Setup

This project requires the following environment variables:

- SECRET_KEY (ex: "123abc#$%")
- DATABASE_URL (ex: "postgresql+psycopg2://user:password@host/vgcatalog")

Create a database called "vgcatalog" on Postgres, and then appy all migrations by running:
`alembic upgrade head` or `make migrate`.

### Running

In the project root, run `fastapi dev app/main.py` or `make run-dev`.
The project will run by default in http://127.0.0.1:8000.

## API docs

After running the project, go to http://127.0.0.1:8000/docs.

## Tests

To run all tests, install all dev dependencies by running `pip install -r requirements.dev.txt` then run `pytest` or
`make test`.

## Code formatting

Install all dev dependencies by running `pip install -r requirements.dev.txt` then run `black .` or
`make code-formatting`.
